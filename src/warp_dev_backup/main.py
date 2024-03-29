import logging
import os
from argparse import Namespace

import humanize
import yaml

from warp_dev_backup import AppContext
from warp_dev_backup.Config import Config
from warp_dev_backup.storage import read_exclusion_file, add_path_to_exclusion_file, create_app_dir, \
    clear_exclusion_file
from warp_dev_backup.tmutil import TMUtil
from warp_dev_backup.treescan import scan_tree

log = logging.getLogger(__name__)


def print_path(context: AppContext, path, path_sentinel_pair):
    if context.cli_args.v > 0:
        path_size = get_size(path)
        context.total_excluded_paths += 1
        context.total_excluded_size += path_size
        print(f"{path_size}\t{path}")
        log.info(f"Found path: {path}, Bytes: {path_size}")
    else:
        print(path)
        log.info(path)


def exclude_path(context: AppContext, path, path_sentinel_pair):
    context.total_excluded_size += os.path.getsize(path)
    context.total_excluded_paths += 1
    TMUtil.exclude_path(context, path)
    add_path_to_exclusion_file(path)


def scan(context: AppContext, start_path):
    config = Config()
    create_app_dir()
    clear_exclusion_file()
    scan_tree(context, config, start_path, exclude_path)


def search(context: AppContext, start_path):
    config = Config()
    if context.cli_args.v > 0:
        print(f'Searching for exclusions in: {start_path}')
    log.info(f'Searching for exclusions in: {start_path}')

    scan_tree(context, config, start_path, print_path)
    if context.cli_args.v > 0:
        print(f'Excluded paths: {context.total_excluded_paths},'
              f' total size: {humanize.naturalsize(context.total_excluded_size, binary=True)}')
    log.info(f'Excluded paths: {context.total_excluded_paths},'
             f' total size: {humanize.naturalsize(context.total_excluded_size, binary=True)}')


def get_size(path='.'):
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        return get_dir_size(path)


def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


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
