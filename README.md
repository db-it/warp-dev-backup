# warp-dev-backup

### Who is it for

warp-dev-backup is a tool for anyone who develops code and backs up their Mac with TimeMachine backups
and wants to reduce backup creation time and disk space requirements.

### What does it do?

This tool automatically searches for development directories such as `node_modules`, `target`, `dist`, etc. and
excludes these paths from the TimeMachine backup.
This reduces the duration and storage space required for the backup.

### How does it work?

It searches in a given path (by default in the home directory) for so-called “sentinels”.
These are known project files such as package.json, pom.xml, setup.py, pyproject.toml, etc.
If a sentinel (e.g. package.json) is found and a defined directory exists (in this case node_modules and/or dist),
then this directory is excluded from the backup.

## Installation

```shell
# Using Homebrew
brew install db-it/tap/warp-dev-backup

# Register and start the warp-dev-backup service to continuously search for paths for exclusion
brew services start db-it/tap/warp-dev-backup

# check if service is registered and scheduled
brew services
```

### Uninstalling

Uninstall warp-dev-backup and undo every exclusion, that warp-dev-backup has excluded form TimeMachine backup.

```shell
# 1. Unregistering service
brew services stop db-it/tap/warp-dev-backup

# 2. un-exclude all excluded paths
cat .warp-dev-backup/excluded_paths |xargs -I {} tmutil removeexclusion {}

# 3. uninstall warp-dev-backup
brew uninstall db-it/tap/warp-dev-backup

# 4. Remove tap
brew untap db-it/tap

# 5. remove app data
rm -rf ~/.warp-dev-backup
```

## Usage

```shell
# Search for directories to be excluded from backup and print them on the console
wdb search -p /start/path

# Start scan from start path and exclude found directories from backup
wdb scan -p /start/path
```

## Config

Config file `~/.warp-dev-backup/config.yml`

```
user:                                       # define your settings as user, to not override the defaults
  start_path: ~/development                 # start search from this path
  exclusion_path_sentinels:                 # define additional  exclusion path sentinels
    - dir: node                             # exclude directory “node” if there is a pom.xml in the same directory
      sentinel: pom.xml
    - dir: dist                             # exclude directory “dist” if there is a setup.py or pyproject.toml in the same directory
      sentinel: setup.py|pyproject.toml     # regex is supported for sentinel definition
  treescan_skip_dirs:                       # skip these directories. NOTE! directory must be relative to start_path
    - project_a                             # e.g. ~/development/project_a is not searched
```

### Default sentinel directory mapping

| Comment            | Sentinel                   | Directory          |
|--------------------|----------------------------|--------------------|
| Maven              | `pom.xml`                  | `target`           |
| Cargo (Rust)       | `Cargo.toml`               | `target`           |
| npm, Yarn (NodeJS) | `package.json`             | `node_modules`     |
| npm, Yarn (NodeJS) | `package.json`             | `dist`             |
| Python             | `setup.py\|pyproject.toml` | `dist`             |
| Python             | `setup.py\|pyproject.toml` | `venv`             |
| Bundler (Ruby)     | `Gemfile`                  | `vendor`           |
| Composer (PHP)     | `composer.json`            | `vendor`           |
| Bower (JavaScript) | `bower.json`               | `bower_components` |
| CocoaPods          | `Podfile`                  | `Pods`             |
| Carthage           | `Cartfile`                 | `Carthage`         |
| Vagrant            | `Vagrantfile`              | `.vagrant`         |
| Stack (Haskell)    | `stack.yaml`               | `.stack-work`      |
| Pub (Dart)         | `pubspec.yaml`             | `.packages`        |
| Swift              | `Package.swift`            | `.build`           |

### Logs

The logfiles of the service are located at `~/Library/Logs/warp-dev-backup`

# Excluded files

To see all excluded paths (not only excluded by warp-dev-backup) from the Time Machine backup, execute the following
command:

```shell
sudo mdfind "com_apple_backup_excludeItem = 'com.apple.backupd'"
```

If a path has been incorrectly excluded from the backup, the excluded path can be removed using the `tmutil` tool.

```shell
tmutil removeexclusion /path/to/directory
```

To ensure that the path is not excluded again in the future, it must also be added to the warp-dev-backup config file.

> **NOTE!** The "treescan skip dir" entry must be relative to the start path!

```yaml
# file: ~/.warp-dev-backup/config.yml
user:
    treescan_skip_dirs:
        - directory-to-exclude
```

## For Developers

### Service

Service plist file is located here `~/Library/LaunchAgents/homebrew.mxcl.warp-dev-backup.plist`
