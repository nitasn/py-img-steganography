from utils import rm_dir_if_exists, colors
from sys import executable as py
from subprocess import Popen, PIPE


def assert_no_error(returncode, err):
  err_text = err.decode().strip()
  if returncode != 0 or err_text != '':
    if err_text:
      print(err_text)
    print(colors.red + 'tests failed :(' + colors.reset)
    exit(1)

try:
  # verify encoder doesn't crash
  p = Popen([py, 'src/main.py', 'encode'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  p.stdin.write(b'assets/dummy_info.json \n assets/cat.png \n output/.tests/cat_with_data.png')
  p.stdin.flush()
  _, err = p.communicate()
  assert_no_error(p.returncode, err)

  # verify decoder doesn't crash
  p = Popen([py, 'src/main.py', 'decode'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  p.stdin.write(b'output/.tests/cat_with_data.png \n output/.tests/decoded_info.json')
  p.stdin.flush()
  _, err = p.communicate()
  assert_no_error(p.returncode, err)
  
  # verify decoded == original
  with open('assets/dummy_info.json', 'rb') as f: original = f.read()
  with open('output/.tests/decoded_info.json', 'rb') as f: decoded = f.read()
  assert decoded == original
  
  print(colors.green + 'tests passed :)' + colors.reset)

finally:
  # cleanup
  rm_dir_if_exists('output/.tests')
