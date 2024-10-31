from utils import rm_dir_if_exists, colors
from sys import executable as py
from subprocess import Popen, PIPE


def assert_no_error(returncode, err):
  err_text = err.decode().strip()
  
  if returncode == 0 and err_text == '':
    return
    
  if err_text:
    print(err_text)
    
  if returncode != 0:
    print(colors.red + 'error:', colors.bold + 'process exited with code', returncode, colors.reset)
    
  print(colors.red + 'tests failed :(' + colors.reset)
  exit(1)


try:
  # verify encoder doesn't crash
  p = Popen([py, 'src/main.py', 'encode'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  p.stdin.write(b'assets/dummy_info.json \n assets/cat.png \n .tests.out/cat_with_data.png')
  p.stdin.flush()
  _, err = p.communicate()
  assert_no_error(p.returncode, err)

  # verify decoder doesn't crash
  p = Popen([py, 'src/main.py', 'decode'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  p.stdin.write(b'.tests.out/cat_with_data.png \n .tests.out/decoded_info.json')
  p.stdin.flush()
  _, err = p.communicate()
  assert_no_error(p.returncode, err)
  
  # verify decoded == original
  with open('assets/dummy_info.json', 'rb') as f: original = f.read()
  with open('.tests.out/decoded_info.json', 'rb') as f: decoded = f.read()
  assert decoded == original
  
  print(colors.green + 'tests passed :)' + colors.reset)

finally:
  # cleanup
  rm_dir_if_exists('.tests.out')
