import os.path

import yaml


class Config:
    _config = {}

    def __init__(self):
        user_settings = {}
        if os.path.exists(self.config_file):
            user_settings = self._read_config_file()

        self._config = {**self._get_default_user_config(), **user_settings, **self._get_app_settings()}

    @property
    def settings(self) -> dict:
        return self._config

    @property
    def app_dir(self):
        return os.path.join(os.path.expanduser('~'), '.warp-dev-backup')

    @property
    def config_file(self):
        return os.path.join(self.app_dir, 'config.yml')

    @property
    def exclusion_path_file(self):
        return self.settings['exclusion_path_file']

    @property
    def exclusion_path_sentinels(self):
        try:
            user_exclusion_path_sentinels = self.get_user_settings()['exclusion_path_sentinels']
        except KeyError:
            user_exclusion_path_sentinels = []
        return self.settings['exclusion_path_sentinels'] + user_exclusion_path_sentinels

    @property
    def exclusion_path_file(self):
        return self.settings['exclusion_path_file']

    def get_user_settings(self):
        return self.settings['user'] if 'user' in self.settings else {}

    def _read_config_file(self):
        with open(self.config_file, 'rt') as f:
            return yaml.safe_load(f.read())

    def _get_app_settings(self):
        return {
            "exclusion_path_file": os.path.join(self.app_dir, "excluded_paths")
        }

    @staticmethod
    def _get_default_user_config():
        return {
            "exclusion_path_sentinels": [
                {"sentinel": "pom.xml", "path": "target"}
            ]
        }
