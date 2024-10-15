import logging
import re
import subprocess

from warp_dev_backup.AppContext import AppContext

logger = logging.getLogger(__name__)


class TMUtil:

    @classmethod
    def path_is_excluded(cls, context: AppContext, path):
        result = subprocess.run(['tmutil', 'isexcluded', path], stdout=subprocess.PIPE)
        tmutil_isexcluded_stdout = result.stdout.decode()
        if context.cli_args.v >= 3:
            logger.debug(f'Subprocess result: {result}')
        match = re.search(r'\[Excluded]', tmutil_isexcluded_stdout)
        return match

    @classmethod
    def exclude_path(cls, context: AppContext, path):
        if cls.path_is_excluded(context, path):
            if context.cli_args.v > 0:
                logger.info(f'Path is already excluded: {path}')
        else:
            command = ['tmutil', 'addexclusion', path]
            result = subprocess.run(command, stdout=subprocess.PIPE)
            if result.returncode == 0:
                logger.info(f'Excluded path: {path}')
            else:
                logger.info(f'Command "{"".join(command)} returned with non zero exit code. " {result.stdout}')
                logger.error(result.stderr)
            return result.returncode
