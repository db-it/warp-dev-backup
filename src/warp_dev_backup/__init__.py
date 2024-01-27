import os

from warp_dev_backup.Logger import Logger

LOGFILE_PATH = os.path.join(os.getcwd(), "wdb.log")
logger = Logger("warp_dev_backup", LOGFILE_PATH).get_logger()
