import os
import re

from warp_dev_backup.AppContext import AppContext


def scan_tree(context: AppContext, start_path, callback):
    for root, dirs, files in os.walk(os.path.expanduser(start_path)):
        dirs[:] = [d for d in dirs if d not in context.config.treescan_skip_dirs]
        for item in context.config.exclusion_path_sentinels:
            if [f for f in files if re.search(item["sentinel"], f)] and item["dir"] in dirs:
                callback(context, os.path.join(root, item["dir"]), item)
                dirs.remove(item["dir"])
