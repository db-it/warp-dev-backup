from argparse import Namespace

from warp_dev_backup.Config import Config


class AppContext:
    cli_args: Namespace
    config: Config
    total_excluded_paths: int
    total_excluded_size: int

    def __init__(self, config: Config, cli_args: Namespace):
        self.cli_args = cli_args
        self.config = config
        self.total_excluded_paths = 0
        self.total_excluded_size = 0
