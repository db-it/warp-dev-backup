import re
import subprocess
import sys

from warp_dev_backup.AppContext import AppContext


class TMUtil:

    @classmethod
    def path_is_excluded(cls, context: AppContext, path):
        result = subprocess.run(['tmutil', 'isexcluded', path], stdout=subprocess.PIPE)
        tmutil_isexcluded_stdout = result.stdout.decode()
        if context.cli_args.v >= 3:
            print(f'[tmutil.path_is_excluded] [DEBUG] Subprocess result: {result}')
        match = re.search(r'\[Excluded]', tmutil_isexcluded_stdout)
        return match

    @classmethod
    def exclude_path(cls, context: AppContext, path):
        if cls.path_is_excluded(context, path):
            if context.cli_args.v > 0:
                print(f'Path is already excluded: {path}')
        else:
            result = subprocess.run(['tmutil', 'addexclusion', path], stdout=subprocess.PIPE)
            if result.returncode == 0:
                print(f'Excluded path: {path}')
            else:
                print(result.stdout)
                print(result.stderr, file=sys.stderr)
            return result.returncode
