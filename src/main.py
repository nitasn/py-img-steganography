from PIL import Image
import numpy as np
import gzip


def read_img_to_array(path: str) -> np.ndarray:
  img = Image.open(path)
  img = img.convert('RGB')
  return np.array(img)


def save_img_array(img: np.ndarray, path: str):
  Image.fromarray(img.astype('uint8'), 'RGB').save(path)


def steganography_encode(img: np.ndarray, msg: bytes) -> np.ndarray:
  original_shape = img.shape
  img = img.flatten()

  # Compress the message using gzip
  compressed_msg = gzip.compress(msg)

  # Decide whether to use compressed message or original message
  if len(compressed_msg) < len(msg):
    use_compression = True
    data_to_encode = compressed_msg
  else:
    use_compression = False
    data_to_encode = msg

  # Build the bits list to encode
  bits = []

  # First bit: compression flag
  bits.append(int(use_compression))

  # Next 63 bits: message length in bytes
  msg_length = len(data_to_encode)
  msg_length_bits = bin(msg_length)[2:].zfill(63)
  bits.extend([int(b) for b in msg_length_bits])

  # Message data bits
  for byte in data_to_encode:
    byte_bits = bin(byte)[2:].zfill(8)
    bits.extend([int(b) for b in byte_bits])

  # Check if the message is too long to encode in the image
  if len(bits) > img.size:
    raise ValueError('Message is too long for this image')

  # Encode the bits into the image
  for bit_index, bit in enumerate(bits):
    img[bit_index] = (img[bit_index] & 0b11111110) | bit

  return img.reshape(original_shape)


def steganography_decode(img: np.ndarray) -> bytes:
  img = img.flatten()

  bit_index = 0

  # Read the first bit: compression flag
  use_compression = img[bit_index] & 1
  bit_index += 1

  # Next 63 bits: message length in bytes
  msg_length_bits = []
  for _ in range(63):
    bit = img[bit_index] & 1
    msg_length_bits.append(str(bit))
    bit_index += 1
  msg_length = int(''.join(msg_length_bits), 2)

  # Extract the message bits
  msg_bits = []
  for _ in range(msg_length * 8):
    bit = img[bit_index] & 1
    msg_bits.append(str(bit))
    bit_index += 1

  # Convert bits to bytes
  msg_bytes = bytearray()
  for i in range(0, len(msg_bits), 8):
    byte_bits = ''.join(msg_bits[i:i+8])
    byte = int(byte_bits, 2)
    msg_bytes.append(byte)

  msg_data = bytes(msg_bytes)

  # If compression was used, decompress the message
  if use_compression:
    msg = gzip.decompress(msg_data)
  else:
    msg = msg_data

  return msg


def test():
  img = read_img_to_array('assets/cat.png')
  
  with open('assets/dummy_info.json', 'rb') as f:
    message = f.read()
  
  encoded_img = steganography_encode(img, message)
  save_img_array(encoded_img, 'assets/cat_encoded.png')
  
  print('Encoded image saved to assets/cat_encoded.png')

  decoded_img = read_img_to_array('assets/cat_encoded.png')
  decoded_message = steganography_decode(decoded_img)
  assert decoded_message == message
  
  print('Decoded message matches the original message')


if __name__ == '__main__':
  test()
