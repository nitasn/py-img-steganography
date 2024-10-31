from input_with_default import input_with_default
from utils import ensure_dir_exists, colors
from PIL import Image
import numpy as np
import questionary
import gzip
import sys
import os


def read_img_to_array(path: str) -> np.ndarray:
  img = Image.open(path)
  img = img.convert('RGB')
  return np.array(img)


def save_img_array(img: np.ndarray, path: str):
  Image.fromarray(img.astype('uint8'), 'RGB').save(path)


def steganography_encode(img: np.ndarray, msg: bytes) -> np.ndarray:
  original_shape = img.shape
  img = img.flatten()
  
  compressed_msg = gzip.compress(msg)

  print(colors.gray, end='')
  print(f'image is large enough for {img.size - 64:,} bytes of data')
  print(f'original message size: {len(msg):,} bytes')
  print(f'compressed message size: {len(compressed_msg):,} bytes')

  if len(compressed_msg) < len(msg):
    print(f"using compression (it results in fewer bytes)")
    using_gzip = True
    data_to_encode = compressed_msg
  else:
    print(f"skipping compression (it doesn't shrink the payload)")
    using_gzip = False
    data_to_encode = msg
  
  print(colors.reset, end='')
  bits = []

  # first bit: compression flag
  bits.append(int(using_gzip))

  # next 63 bits: message length in bytes
  msg_length = len(data_to_encode)
  msg_length_bits = bin(msg_length)[2:].zfill(63)
  bits.extend([int(b) for b in msg_length_bits])

  # rest of the bits: actual payload
  for byte in data_to_encode:
    byte_bits = bin(byte)[2:].zfill(8)
    bits.extend([int(b) for b in byte_bits])

  if len(bits) > img.size:
    raise ValueError('message is too long for this image')

  for bit_index, bit in enumerate(bits):
    img[bit_index] = (img[bit_index] & 0b11111110) | bit

  return img.reshape(original_shape)


def steganography_decode(img: np.ndarray) -> bytes:
  img = img.flatten()

  bit_index = 0

  # read the first bit: compression flag
  using_gzip = img[bit_index] & 1
  bit_index += 1

  # next 63 bits: message length in bytes
  msg_length_bits = []
  for _ in range(63):
    bit = img[bit_index] & 1
    msg_length_bits.append(str(bit))
    bit_index += 1
  msg_length = int(''.join(msg_length_bits), 2)

  # extract the payload bits
  msg_bits = []
  for _ in range(msg_length * 8):
    bit = img[bit_index] & 1
    msg_bits.append(str(bit))
    bit_index += 1

  # convert bits to bytes
  msg_bytes = bytearray()
  for i in range(0, len(msg_bits), 8):
    byte_bits = ''.join(msg_bits[i:i+8])
    byte = int(byte_bits, 2)
    msg_bytes.append(byte)

  msg_data = bytes(msg_bytes)
  msg = gzip.decompress(msg_data) if using_gzip else msg_data

  return msg


def get_path_from_user(prompt: str, default: str, ensure_exists=False) -> str:
  res = input_with_default(prompt + ": ", default)
  res = res.strip().strip('"').strip("'")
  if not res:
    res = default
  if ensure_exists and not os.path.exists(res):
    print(colors.red + 'path does not exist:', res + colors.reset)
    exit(1)
  return res


def encode():
  input_msg_path = 'assets/dummy_info.json'
  input_img_path = 'assets/cat.png'
  output_img_path = 'output/cat_with_data.png'
  
  input_msg_path = get_path_from_user('input data path', input_msg_path, ensure_exists=True)
  input_img_path = get_path_from_user('input image path', input_img_path, ensure_exists=True)
  output_img_path = get_path_from_user('output image path', output_img_path)
  
  img = read_img_to_array(input_img_path)
  msg = open(input_msg_path, 'rb').read()
  
  ensure_dir_exists(output_img_path)
  img = steganography_encode(img, msg)
  save_img_array(img, output_img_path)
  
  print('encoded image saved to', colors.bold + output_img_path + colors.reset)


def decode():
  input_img_path = 'output/cat_with_data.png'
  output_msg_path = 'output/decoded_info.json'
  
  input_img_path = get_path_from_user('input image path', input_img_path, ensure_exists=True)
  output_msg_path = get_path_from_user('output message path', output_msg_path)
  
  img = read_img_to_array(input_img_path)
  msg = steganography_decode(img)
  
  ensure_dir_exists(output_msg_path)
  with open(output_msg_path, 'wb') as f:
    f.write(msg)
  
  print('decoded message saved to', colors.bold + output_msg_path + colors.reset)


def main():
  if len(sys.argv) != 2 or sys.argv[1] not in ('encode', 'decode'):
    print(f'usage: py {sys.argv[0]} <encode|decode>')
    exit(1)
  
  match sys.argv[1]:
    case 'encode': encode()
    case 'decode': decode()


if __name__ == '__main__':
  main()
