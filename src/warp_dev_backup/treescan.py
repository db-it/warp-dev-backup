import os
import re

from warp_dev_backup.AppContext import AppContext


def scan_tree(context: AppContext, start_path, callback):
    abspath = os.path.abspath(os.path.expanduser(start_path))
    if not os.path.exists(abspath):
        raise FileNotFoundError(f"The specified path {abspath} does not exist.")
    for root, dirs, files in os.walk(abspath):
        dirs[:] = [d for d in dirs if d not in context.config.treescan_skip_dirs]
        for item in context.config.exclusion_path_sentinels:
            if [f for f in files if re.search(item["sentinel"], f)] and item["dir"] in dirs:
                callback(context, os.path.join(root, item["dir"]), item)
                dirs.remove(item["dir"])
