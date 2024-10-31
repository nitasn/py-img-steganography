import os
import shutil


def ensure_dir_exists(path: str):
  ''' performs `mkdir -p` on the directory part of the path '''
  os.makedirs(os.path.dirname(path), exist_ok=True)


def rm_dir_if_exists(path: str):
  ''' performs `rm -rf`, assuming path is a directory '''
  if os.path.exists(path):
    shutil.rmtree(path)


class colors:
  red    = '\033[31m'
  green  = '\033[32m'
  blue   = '\033[34m'
  yellow = '\033[33m'
  gray   = '\033[90m'
  bold   = '\033[1m'
  reset  = '\033[0m'
