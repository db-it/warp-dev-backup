from unittest.mock import patch, Mock

import warp_dev_backup
from warp_dev_backup.Config import Config


class TestConfig:

    def test_settings__returns_default_user_settings(self):
        config = Config()
        with patch.object(Config, 'exclusion_path_sentinels', [
            {'sentinel': 'pom.xml', 'dir': 'target'},
        ]):
            sentinels = config.exclusion_path_sentinels

        assert sentinels == [{'dir': 'target', 'sentinel': 'pom.xml'}]
        assert config.exclusion_path_file.endswith('.warp-dev-backup/excluded_paths')

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

    def test_app_dir(self):
        assert Config().app_dir.endswith('.warp-dev-backup')

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
            'exclusion_path_sentinels': [{'sentinel': 'pom.xml', 'dir': 'target'},],
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
