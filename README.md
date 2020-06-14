# Installation

In a virtualenv: `pip install -r requirements.txt`


# Configuration

## API access

1. In OPNsense UI, Create dedicated account with access to alias section and add a key.
2. Add private key in keyring: `keyring set opnsense_alias_updater <KEY_ID>`

## Networks.yml file

1. Copy example: `cp networks.example.yml networks.yml`
2. Update different entries
