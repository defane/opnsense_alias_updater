# Installation

In a virtualenv: `pip install -r requirements.txt`

# Configuration

## API access

1. With OPNsense UI, create dedicated account with access to alias section and add a key.
2. Add private key in keyring: `keyring set opnsense_alias_updater <KEY_ID>`

## Networks.yml file

1. Copy example: `cp networks.example.yml networks.yml`
2. Update different entries

# Usage

```
./cli.py
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  clean  Remove unreferenced autogenerated aliases.
  push   Push autogenerated aliases on firewall and apply them.
```
