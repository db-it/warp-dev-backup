import logging
import os

from warp_dev_backup.AppContext import AppContext
from warp_dev_backup.Config import Config

log = logging.getLogger(__name__)


def scan_tree(context: AppContext, start_path, exclusion_path_sentinels, callback):
    skip_dirs = Config().treescan_skip_dirs

    for root, dirs, files in os.walk(os.path.expanduser(start_path)):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for item in exclusion_path_sentinels:
            if item["sentinel"] in files and item["path"] in dirs:
                callback(context, os.path.join(root, item["path"]), item)
                dirs.remove(item["path"])
