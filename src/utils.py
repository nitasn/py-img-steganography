import os
import shutil


def ensure_dir_exists(path: str):
  os.makedirs(os.path.dirname(path), exist_ok=True)


def rm_rf(path: str):
  if os.path.exists(path):
    shutil.rmtree(path)
