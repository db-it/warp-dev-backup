import os
from pathlib import Path

from warp_dev_backup.Config import Config

EXCLUDED_PATHS_FILE = Path(Config().exclusion_path_file).expanduser()


def read_exclusion_file():
    with open(EXCLUDED_PATHS_FILE, "r") as f:
        return f.read().splitlines()


def add_path_to_exclusion_file(path):
    with open(EXCLUDED_PATHS_FILE, "a") as f:
        f.write(f"{path}\n")


def clear_exclusion_file():
    if os.path.exists(EXCLUDED_PATHS_FILE):
        os.remove(EXCLUDED_PATHS_FILE)
