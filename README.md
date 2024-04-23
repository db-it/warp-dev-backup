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
