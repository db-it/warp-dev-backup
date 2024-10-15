import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class LoggerFactory:
    _debug: bool
    _logfile_path: (Path, str)

    def __init__(self, logger_name, log_level_name='INFO', debug=False, logfile_path: (Path, str) = None) -> None:
        self._logger_name = logger_name
        if isinstance(logfile_path, str):
            self._logfile_path = Path(logfile_path)
        else:
            self._logfile_path = logfile_path

        self._debug = debug

        self.logger = logging.getLogger(self._logger_name)
        self.logger.setLevel(logging.getLevelName(log_level_name))
        if self._logfile_path:
            self.logger.addHandler(self._setup_file_handler())
        self.logger.addHandler(self._setup_console_handler())
        self.logger.propagate = False

    def _setup_console_handler(self):
        ch = logging.StreamHandler()
        ch.setLevel(level=logging.DEBUG)
        ch.setFormatter(self._get_console_formatter())
        return ch

    def _setup_file_handler(self, formatter=None):
        # if os.access(os.path.dirname(self._logfile_path), os.W_OK):
        fh = TimedRotatingFileHandler(self._logfile_path, when="midnight", interval=1, backupCount=5)
        fh.setLevel(level=logging.DEBUG)
        if not formatter:
            formatter = self._get_file_formatter()
        fh.setFormatter(formatter)
        return fh
        # else:
        #     print(f"Error creating logfile. {self._logfile_path}", file=sys.stderr)
        #     exit(1)

    def _get_console_formatter(self):
        if self._debug:
            return logging.Formatter('[%(name)s:%(lineno)d] %(message)s')
        return logging.Formatter('%(message)s')

    @staticmethod
    def _get_file_formatter():
        return logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
