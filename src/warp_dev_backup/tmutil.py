import logging
import re
import subprocess

from warp_dev_backup.AppContext import AppContext


class TMUtil:

    @classmethod
    def path_is_excluded(cls, path):
        result = subprocess.run(['tmutil', 'isexcluded', path], stdout=subprocess.PIPE)
        tmutil_isexcluded_stdout = result.stdout.decode()
        logging.debug(f"Subprocess result: {result}")
        match = re.search(r'\[Excluded]', tmutil_isexcluded_stdout)
        return match

    @classmethod
    def exclude_path(cls, context: AppContext, path):
        if cls.path_is_excluded(path):
            logging.info(f"Path is already excluded: {path}")
            if context.cli_args.v > 0:
                print(f"Path is already excluded: {path}")
        else:
            result = subprocess.run(['tmutil', 'addexclusion', path], stdout=subprocess.PIPE)
            if result.returncode == 0:
                logging.info(f"Excluded path: {path}")
            else:
                logging.error(result.stdout)
                logging.error(result.stderr)
            return result.returncode
