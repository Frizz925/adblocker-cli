[![Build Status](https://travis-ci.org/Frizz925/adblocker-cli.svg?branch=master)](https://travis-ci.org/Frizz925/adblocker-cli)
[![codecov](https://codecov.io/gh/Frizz925/adblocker-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/Frizz925/adblocker-cli)

# AdBlocker CLI
Update your hosts file from adblock filters

## Requirements
- Python 2 or 3

## Installation
```sh
git clone https://github.com/Frizz925/adblocker-cli.git adblocker-cli
cd adblocker-cli
pip install .
```

## Usage
```sh
# Add filter list to /etc/hosts (requires root)
sudo adblocker add
# Remove filter list from /etc/hosts (requires root)
sudo adblocker remove
```
