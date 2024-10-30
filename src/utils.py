import os
import shutil


def ensure_dir_exists(path: str):
  ''' performs `mkdir -p` on the directory part of the path '''
  os.makedirs(os.path.dirname(path), exist_ok=True)


def rm_dir_if_exists(path: str):
  ''' performs `rm -rf`, assuming path is a directory '''
  if os.path.exists(path):
    shutil.rmtree(path)
