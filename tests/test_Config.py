from pathlib import Path
from unittest.mock import patch, Mock

from warp_dev_backup.Config import Config


class TestConfig:

    def test_config_file__returns_user_defined_path(self):
        config = Config(config_file='/myconfig/file')

        assert config.config_file.as_posix() == '/myconfig/file'

    def test_config_file__returns_default_path(self):
        config = Config()

        assert config.config_file.as_posix() == '~/.warp-dev-backup/config.yml'

    def test_app_dir(self):
        assert Config().app_dir == Path('~/.warp-dev-backup')

    def test_settings__returns_default_user_settings(self):
        config = Config()
        with patch.object(Config, 'exclusion_path_sentinels', [
            {'sentinel': 'pom.xml', 'dir': 'target'},
        ]):
            sentinels = config.exclusion_path_sentinels

        assert sentinels == [{'dir': 'target', 'sentinel': 'pom.xml'}]
        assert config.exclusion_path_file.endswith('.warp-dev-backup/excluded_paths')

    def test_start_path__returns_default_user_settings_start_path(self, config4test):
        config = config4test(config_file='/non/existent/configfile')

        assert config.start_path == Path('~/')

    def test_start_path__returns_user_settings_start_path(self, config4test):
        config = config4test()

        assert config.start_path == Path('~/custom/test/start/path')

    @patch("os.path.exists", Mock(return_value=True))
    @patch.object(Config, '_read_config_file', autospec=True)
    def test_settings__user_config_file_only_overrides_user_defaults(self, mock_read_config_file: Mock):
        mock_read_config_file.return_value = {
            'exclusion_path_file': '/overridden/path',
            'exclusion_path_sentinels': [{'dir': 'node_modules', 'sentinel': 'package.json'}]
        }

        settings = Config().settings

        assert settings['exclusion_path_file'].endswith('.warp-dev-backup/excluded_paths')
        assert settings['exclusion_path_sentinels'] == [{'dir': 'node_modules', 'sentinel': 'package.json'}]

    @patch("os.path.exists", Mock(return_value=False))
    @patch.object(Config, '_read_config_file', autospec=True)
    def test_get_user_settings__returns_empty_dict(self, _):
        assert Config().get_user_settings() == {}

    @patch("os.path.exists", Mock(return_value=True))
    @patch.object(Config, '_read_config_file', autospec=True)
    def test_get_user_settings__returns_user_settings(self, mock_read_config_file: Mock):
        mock_read_config_file.return_value = {
            'user': {
                'exclusion_path_sentinels': [{'dir': 'node_modules', 'sentinel': 'package.json'}]
            }
        }

        assert Config().get_user_settings() == {
            'exclusion_path_sentinels': [{'dir': 'node_modules', 'sentinel': 'package.json'}]
        }

    @patch("os.path.exists", Mock(return_value=True))
    @patch.object(Config, '_read_config_file', autospec=True)
    def test_exclusion_path_sentinels__returns_aggregated_list(self, mock_read_config_file: Mock):
        mock_read_config_file.return_value = {
            'exclusion_path_sentinels': [{'sentinel': 'pom.xml', 'dir': 'target'}, ],
            'user': {
                'exclusion_path_sentinels': [{'dir': 'node_modules', 'sentinel': 'package.json'}]
            }
        }

        sentinels = Config().exclusion_path_sentinels
        assert sentinels == [
            {"dir": "target", "sentinel": "pom.xml"},
            {'dir': 'node_modules', 'sentinel': 'package.json'}
        ]

    @patch("os.path.exists", Mock(return_value=False))
    @patch.object(Config, '_read_config_file', autospec=True)
    def test_exclusion_path_sentinels__returns_without_user_settings(self, mock_read_config_file: Mock):
        with patch.object(Config, 'exclusion_path_sentinels', [
            {'sentinel': 'pom.xml', 'dir': 'target'},
        ]):
            sentinels = Config().exclusion_path_sentinels

        assert sentinels == [
            {"dir": "target", "sentinel": "pom.xml"}
        ]
