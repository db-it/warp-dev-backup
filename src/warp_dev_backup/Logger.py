import logging


class Logger:
    def __init__(self, logger_name, logfile_path=None) -> None:
        super().__init__()
        self._logger_name = logger_name
        self._logfile_path = logfile_path

    def get_logger(self):
        logger = logging.getLogger(self._logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self._setup_file_handler())
        # logger.addHandler(self._setup_console_handler())
        logger.propagate = False
        return logger

    def _setup_console_handler(self):
        ch = logging.StreamHandler()
        ch.setLevel(level=logging.DEBUG)
        ch.setFormatter(self._get_console_formatter())
        return ch

    def _setup_file_handler(self, formatter=None):
        if self._logfile_path and isinstance(self._logfile_path, str):
            # if os.access(os.path.dirname(self._logfile_path), os.W_OK):
            fh = logging.FileHandler(self._logfile_path)
            fh.setLevel(level=logging.DEBUG)
            if not formatter:
                formatter = self._get_file_formatter()
            fh.setFormatter(formatter)
            return fh
            # else:
            #     print(f"Error creating logfile. {self._logfile_path}", file=sys.stderr)
            #     exit(1)

    @staticmethod
    def _get_console_formatter():
        # TODO Set format with line numbers, when loglevel is DEBUG
        # return logging.Formatter('%(log_color)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s')
        return logging.Formatter('[%(levelname)s] %(message)s')

    @staticmethod
    def _get_file_formatter():
        return logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
