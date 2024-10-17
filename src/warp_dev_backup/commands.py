import logging
import os

import humanize
import yaml

import warp_dev_backup.storage as storage
from warp_dev_backup import AppContext
from warp_dev_backup.Config import Config
from warp_dev_backup.tmutil import TMUtil
from warp_dev_backup.treescan import scan_tree

logger = logging.getLogger(__name__)


class Command:

    def __init__(self, context):
        self.context: AppContext = context

    @staticmethod
    def print_path(context: AppContext, path, path_sentinel_pair):
        if context.cli_args.v >= 1:
            path_size = Command.__get_size(path)
            context.total_excluded_paths += 1
            context.total_excluded_size += path_size
            logger.info(f"{humanize.naturalsize(path_size, gnu=True):>10}\t{path}")
        else:
            logger.info(path)

    @staticmethod
    def exclude_path(context: AppContext, path, path_sentinel_pair):
        context.total_excluded_size += os.path.getsize(path)
        context.total_excluded_paths += 1
        TMUtil.exclude_path(context, path)
        storage.add_path_to_exclusion_file(path)

    def scan(self):
        start_path = self.__get_start_path(self.context)
        storage.clear_exclusion_file()
        scan_tree(self.context, start_path, self.exclude_path)

    def search(self):
        start_path = self.__get_start_path(self.context)

        if self.context.cli_args.v >= 1:
            logger.info(f'Searching for exclusions in: {start_path}')

        scan_tree(self.context, start_path, self.print_path)
        if self.context.cli_args.v >= 1:
            logger.info(f'Excluded paths: {self.context.total_excluded_paths}')
            logger.info(f'Total excluded size: {humanize.naturalsize(self.context.total_excluded_size, gnu=True)}')

    @staticmethod
    def get_total_size_of_excluded_path():
        total_size = 0
        excluded_paths = storage.read_exclusion_file()

        for path in excluded_paths:
            path_size = os.path.getsize(path)
            total_size += path_size
        return total_size

    @staticmethod
    def print_config(config: Config):
        logger.info(yaml.dump(config.settings))

    @staticmethod
    def __get_size(path='.'):
        if os.path.isfile(path):
            return os.path.getsize(path)
        elif os.path.isdir(path):
            return Command.__get_dir_size(path)

    @staticmethod
    def __get_dir_size(path='.'):
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += Command.__get_dir_size(entry.path)
        return total

    @staticmethod
    def __get_start_path(context: AppContext):
        if context.cli_args.start_path:
            return context.cli_args.start_path
        else:
            return context.config.start_path
