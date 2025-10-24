import os
import shutil
from typing import List


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def cleanup_files(paths: List[str]):
    for path in paths:
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"Error cleaning up {path}: {e}")


def get_file_size(path: str) -> int:
    try:
        return os.path.getsize(path)
    except Exception:
        return 0
