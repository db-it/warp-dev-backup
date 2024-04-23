# warp-dev-backup

## Usage

```shell
# Search for directories to be excluded from backup and print them on the console
wdb search -p /start/path

# Start scan from start path and exclude found directories from backup
wdb scan -p /start/path
```

## Config

Config file `~/.warp-dev-backup/config.yml`

## Service

Service plist file is located here `~/Library/LaunchAgents/homebrew.mxcl.warp-dev-backup.plist`

### Logs

The logfiles of the service are located at `~/Library/Logs/warp-dev-backup`


# Excluded files
To see all excluded paths from the Time Machine backup, execute the following command:

```shell
sudo mdfind "com_apple_backup_excludeItem = 'com.apple.backupd'"
```

If a path has been incorrectly excluded from the backup, the excluded path can be removed using the `tmutil` tool.

```shell
tmutil removeexclusion /path/to/directory
```

To ensure that the path is not excluded again in the future, it must also be added to the warp-dev-backup config file.

```yaml
# file: ~/.warp-dev-backup/config.yml
user:
  treescan_skip_dirs:
    - /path/to/exclude
```
