from argparse import Namespace
from pathlib import Path

import pytest

from warp_dev_backup.AppContext import AppContext
from warp_dev_backup.Config import Config


@pytest.fixture
def context(config4test, argparse_namespace):
    def _context(config=None, cli_args=None):
        if config is None:
            config = config4test()
        if cli_args is None:
            cli_args = argparse_namespace()
        return AppContext(config, cli_args)

    return _context


@pytest.fixture
def config4test():
    test_dir = Path(__file__).parent

    def _test_config(config_file=None):
        if config_file is None:
            config_file = test_dir / 'test_data' / 'test.config.yml'
        return Config(config_file=config_file)

    return _test_config


@pytest.fixture
def argparse_namespace():
    def _argparse_namespace(overrides=None):
        namespace_defaults = {
            'command': 'search',
            'config': None,
            'quiet': False,
            'start_path': '~/',
            'v': 0,
        }
        if overrides is None:
            overrides = {}
        return Namespace(**{**namespace_defaults, **overrides})

    return _argparse_namespace
