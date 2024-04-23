from argparse import Namespace


class TestArgparseNamespace:

    def test_should_return_defaults(self, argparse_namespace):
        namespace = argparse_namespace()

        assert namespace == Namespace(**{
            'command': 'search',
            'config': None,
            'quiet': False,
            'start_path': '~/',
            'v': 0,
        })

    def test_should_partial_override_defaults(self, argparse_namespace):
        namespace = argparse_namespace(overrides={
            'command': 'scan',
            'quiet': True,
            'start_path': '~/changed/path',
        })

        assert namespace == Namespace(**{
            'command': 'scan',
            'config': None,
            'quiet': True,
            'start_path': '~/changed/path',
            'v': 0,
        })
