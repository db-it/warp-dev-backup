import logging
import os

from warp_dev_backup.AppContext import AppContext

log = logging.getLogger(__name__)


def scan_tree(context: AppContext, start_path, exclusion_path_sentinels, callback):
    for root, dirs, files in os.walk(os.path.expanduser(start_path)):
        for item in exclusion_path_sentinels:
            if item["sentinel"] in files and item["path"] in dirs:
                callback(context, os.path.join(root, item["path"]), item)
                dirs.remove(item["path"])
