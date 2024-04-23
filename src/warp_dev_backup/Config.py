import os.path
from pathlib import Path

import yaml


class Config:
    _config: dict

    def __init__(self, config_file=None):
        if config_file:
            self._config_file = Path(config_file)
        else:
            self._config_file = self.app_dir / 'config.yml'

        user_settings = {}
        if self.config_file.expanduser().exists():
            user_settings = self._read_config_file()

        self._config = {**self._get_default_user_config(), **user_settings, **self._get_app_settings()}

    @property
    def settings(self) -> dict:
        return self._config

    def get_user_settings(self):
        return self.settings['user'] if 'user' in self.settings else {}

    @property
    def config_file(self) -> Path:
        return self._config_file

    @property
    def app_dir(self) -> Path:
        return Path('~/.warp-dev-backup')

    @property
    def exclusion_path_file(self):
        return self.settings['exclusion_path_file']

    @property
    def start_path(self) -> Path:
        try:
            start_path = self.get_user_settings()['start_path']
            return Path(start_path)
        except KeyError:
            return Path(self.settings['start_path'])

    @property
    def exclusion_path_sentinels(self):
        try:
            user_exclusion_path_sentinels = self.get_user_settings()['exclusion_path_sentinels']
        except KeyError:
            user_exclusion_path_sentinels = []
        return self.settings['exclusion_path_sentinels'] + user_exclusion_path_sentinels

    @property
    def treescan_skip_dirs(self):
        try:
            treescan_skip_dirs = self.get_user_settings()['treescan_skip_dirs']
        except KeyError:
            treescan_skip_dirs = []
        return self.settings['treescan_skip_dirs'] + treescan_skip_dirs

    def _read_config_file(self):
        with open(self.config_file.expanduser(), 'rt') as f:
            return yaml.safe_load(f.read())

    def _get_app_settings(self):
        return {
            'exclusion_path_file': os.path.join(self.app_dir, 'excluded_paths')
        }

    @staticmethod
    def _get_default_user_config():
        return {
            'start_path': '~/',
            'exclusion_path_sentinels': [
                {'sentinel': 'pom.xml', 'dir': 'target'},  # Maven
                {'sentinel': 'Cargo.toml', 'dir': 'target'},  # Cargo (Rust)
                {'sentinel': 'package.json', 'dir': 'node_modules'},  # npm, Yarn (NodeJS)
                {'sentinel': 'package.json', 'dir': 'dist'},  # npm, Yarn (NodeJS)
                {'sentinel': 'setup.py|pyproject.toml', 'dir': 'dist'},  # Python
                {'sentinel': 'setup.py|pyproject.toml', 'dir': 'venv'},  # Python
                {'sentinel': 'Gemfile', 'dir': 'vendor'},  # Bundler (Ruby)
                {'sentinel': 'composer.json', 'dir': 'vendor'},  # Composer (PHP)
                {'sentinel': 'bower.json', 'dir': 'bower_components'},  # Bower (JavaScript)
                {'sentinel': 'Podfile', 'dir': 'Pods'},  # CocoaPods
                {'sentinel': 'Cartfile', 'dir': 'Carthage'},  # Carthage
                {'sentinel': 'Vagrantfile', 'dir': '.vagrant'},  # Vagrant
                {'sentinel': 'stack.yaml', 'dir': '.stack-work'},  # Stack (Haskell)
                {'sentinel': 'pubspec.yaml', 'dir': '.packages'},  # Pub (Dart)
                {'sentinel': 'Package.swift', 'dir': '.build'},  # Swift
            ],
            'treescan_skip_dirs': [
                'Library',
                '.Trash',
            ],
        }
