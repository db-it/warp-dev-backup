from argparse import Namespace


class AppContext:

    total_excluded_paths: int
    total_excluded_size: int
    cli_args: Namespace

    def __init__(self):
        self.cli_args = Namespace()
        self.total_excluded_paths = 0
        self.total_excluded_size = 0
