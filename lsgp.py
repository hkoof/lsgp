#!/usr/env/bin python

__program__ = "lsgp"
__version__ = "0.01"

if __name__ != "__main__":
    raise ImportError("Program not importable.")

import sys
import argparse
import configparser
from collections import OrderedDict


#### Command line parsing
#
parser = argparse.ArgumentParser(prog=__program__,
        description="LDAP Server Gauge Panel - Text mode interface to cn=monitor."
    )
parser.add_argument("-c", "--config", type=argparse.FileType('r'),
        help="path of configuration file",
    )
parser.add_argument("--print-config", action='store_true',
        help="print configuration to standard output and exit",
    )
args = parser.parse_args()


#### Config file parsing
#
config = configparser.ConfigParser(dict_type=OrderedDict)
config['lsgp'] = {
        'interval': 2,
        }

config['monitor'] = {
    'url': 'ldapi:///',
    'ssl': 'no',
    'auth': 'SIMPLE',
    'binddn': '',
    'password': '',
}

if args.config is not None:
    config.read_file(args.config)

if args.print_config:
    config.write(sys.stdout)
    sys.exit(0)

import lsgptui

