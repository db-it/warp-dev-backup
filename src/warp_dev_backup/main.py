import logging
import os
from argparse import Namespace

import humanize
import yaml

from warp_dev_backup.Config import Config
from warp_dev_backup.storage import read_exclusion_file, add_path_to_exclusion_file, create_app_dir, \
    clear_exclusion_file
from warp_dev_backup.tmutil import TMUtil
from warp_dev_backup.treescan import scan_tree

log = logging.getLogger(__name__)


def print_path(context, path, path_sentinel_pair):
    if context.v > 0:
        path_size = os.path.getsize(path)
        print(f"{path_size}\t{path}")
        log.info(f"Found path: {path}, Bytes: {path_size}")
    else:
        print(path)
        log.info(path)


def my_callback(context, path, path_sentinel_pair):
    TMUtil.exclude_path(path, context)
    add_path_to_exclusion_file(path)


def scan(context, start_path):
    create_app_dir()
    clear_exclusion_file()
    scan_tree(context, start_path, Config().exclusion_path_sentinels, my_callback)


def search(context, start_path):
    if context.v > 0:
        print(f"Searching for exclusions in: {start_path}")
    log.info(f"Searching for exclusions in: {start_path}")

    scan_tree(context, start_path, Config().exclusion_path_sentinels, print_path)
    if context.v > 0:
        print(f"Total size of excluded paths: {humanize.naturalsize(get_total_size_of_excluded_path(), binary=True)}")
    log.info(f"Total size of excluded paths: {humanize.naturalsize(get_total_size_of_excluded_path(), binary=True)}")


def get_total_size_of_excluded_path():
    total_size = 0
    excluded_paths = read_exclusion_file()

    for path in excluded_paths:
        path_size = os.path.getsize(path)
        total_size += path_size
    return total_size


def print_config():
    print(yaml.dump(Config().settings))


if __name__ == "__main__":
    scan(Namespace(v=0), "~/tmp")
