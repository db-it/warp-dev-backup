from unittest import mock
from unittest.mock import Mock, call, MagicMock

import pytest

from warp_dev_backup.Config import Config
from warp_dev_backup.treescan import scan_tree


def test_should_invoke_callback_with_params(context):
    config = MagicMock(spec=Config)
    config.exclusion_path_sentinels = [
        {'sentinel': 'pyproject.toml', 'dir': 'venv'},
    ]
    context = context(config)
    start_path = '/dev'
    mock_callback = Mock()

    with mock.patch('os.walk') as mock_walk:
        mock_walk.return_value = [
            ['/dev', ['python-project', ], []],
            ['/dev/python-project', ['venv', 'dist', ], ['pyproject.toml', ]],
        ]
        scan_tree(context, start_path, mock_callback)

    assert mock_callback.call_args == call(
        context,
        '/dev/python-project/venv',
        {'sentinel': 'pyproject.toml', 'dir': 'venv'}
    )


@pytest.mark.parametrize('sentinel_files', [
    pytest.param(['pyproject.toml', ], id='pyproject.toml'),
    pytest.param(['setup.py', ], id='setup.py'),
    pytest.param(['setup.cfg', ], id='setup.cfg'),
])
def test_should_invoke_callback_on_sentinel_match_by_regex(sentinel_files, context):
    config = MagicMock(spec=Config)
    config.exclusion_path_sentinels = [
        {'sentinel': r'pyproject.toml|setup.[py|cfg]', 'dir': 'venv'},
    ]
    context = context(config)
    start_path = '/dev'
    mock_callback = Mock()

    with mock.patch('os.walk') as mock_walk:
        mock_walk.return_value = [
            ['/dev', ['python-project', ], []],
            ['/dev/python-project', ['venv', 'dist', ], sentinel_files],
        ]
        scan_tree(context, start_path, mock_callback)

    assert mock_callback.call_args == call(
        context,
        '/dev/python-project/venv',
        {'sentinel': r'pyproject.toml|setup.[py|cfg]', 'dir': 'venv'},
    )


def test_should_not_invoke_callback_on_non_existent_sentinel_or_dir(context):
    config = MagicMock(spec=Config)
    config.exclusion_path_sentinels = [
        {'sentinel': r'pyproject.toml|setup.[py|cfg]', 'dir': 'venv'},
    ]
    context = context(config)
    start_path = '/dev'
    mock_callback = Mock()

    with mock.patch('os.walk') as mock_walk:
        mock_walk.return_value = [
            ['/dev', ['python-project', ], []],
            ['/dev/python-project', ['venv', 'dist', ], []],
            ['/dev/python-project', [], ['setup.py']],
        ]
        scan_tree(context, start_path, mock_callback)

    assert mock_callback.call_count == 0
