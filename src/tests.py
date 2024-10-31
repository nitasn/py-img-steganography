from utils import rm_dir_if_exists, colors
from sys import executable as py
from subprocess import Popen, PIPE


try:
  # verify encoder doesn't crash
  p = Popen([py, 'src/main.py', 'encode'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  p.stdin.write(b'assets/dummy_info.json \n assets/cat.png \n output/.tests/cat_with_data.png')
  p.stdin.flush()
  _, err = p.communicate()
  assert p.returncode == 0 and err.decode().strip() == ''

  # verify decoder doesn't crash
  p = Popen([py, 'src/main.py', 'decode'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  p.stdin.write(b'output/.tests/cat_with_data.png \n output/.tests/decoded_info.json')
  p.stdin.flush()
  _, err = p.communicate()
  assert p.returncode == 0 and err.decode().strip() == ''
  
  # verify decoded == original
  with open('assets/dummy_info.json', 'rb') as f: original = f.read()
  with open('output/.tests/decoded_info.json', 'rb') as f: decoded = f.read()
  assert decoded == original
  
  print(colors.green + 'tests passed :)' + colors.reset)

finally:
  # cleanup
  rm_dir_if_exists('output/.tests')
