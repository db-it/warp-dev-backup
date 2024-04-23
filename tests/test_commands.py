from unittest.mock import patch, Mock, call

import warp_dev_backup.commands
from warp_dev_backup.commands import Command


class TestCommand:

    @patch('warp_dev_backup.commands.storage.clear_exclusion_file', autospec=True)
    @patch.object(warp_dev_backup.commands.Command, 'exclude_path')
    @patch('warp_dev_backup.commands.scan_tree', autospec=True)
    def test_scan(self, mock_scan_tree: Mock, mock_exclude_path: Mock, mock_clear_exclusion_file: Mock, context):
        app_context = context()
        command = Command(app_context)

        command.scan()

        assert mock_scan_tree.call_count == 1
        assert mock_scan_tree.call_args_list == [
            call(app_context, '~/', mock_exclude_path)
        ]
        assert mock_clear_exclusion_file.call_count == 1

    @patch.object(warp_dev_backup.commands.Command, 'print_path')
    @patch('warp_dev_backup.commands.scan_tree', autospec=True)
    def test_search(self, mock_scan_tree: Mock, mock_print_path: Mock, context):
        app_context = context()
        command = Command(app_context)

        command.search()

        assert mock_scan_tree.call_count == 1
        assert mock_scan_tree.call_args_list == [
            call(app_context, '~/', mock_print_path)
        ]
