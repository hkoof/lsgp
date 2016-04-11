#!/usr/env/bin python

__program__ = "lsgp"
__version__ = "0.01"

if __name__ != "__main__":
    raise ImportError("Program not importable.")

import sys
import os.path
import argparse

from config import Config

#### Command line parsing
#
parser = argparse.ArgumentParser(prog=__program__,
        description="LDAP Server Gauge Panel - Text mode interface to cn=monitor."
    )
parser.add_argument("-c", "--config",
        default=['/etc/lsgp.conf', os.path.expanduser('~/.lsgprc')],
        help="path of configuration file",
    )
parser.add_argument("--print-config", action='store_true',
        help="print configuration to standard output and exit",
    )
args = parser.parse_args()

conf = Config(args.config)
monitorconf = conf['monitor']

if args.print_config:
    conf.write(sys.stdout)
    sys.exit(0)


