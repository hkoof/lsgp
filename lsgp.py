#!/usr/env/bin python

if __name__ != "__main__":
    raise ImportError("Program not importable.")

import sys
import os.path
import argparse

import prog
from config import Config

#### Command line parsing
#
parser = argparse.ArgumentParser(prog=__program__,
        description=prog.description,
    )
parser.add_argument('-V', '--version',
        action='version',
        version='%(prog)s {}'.format(__version__),
    )
parser.add_argument("-c", "--config",
        default=['/etc/lsgp.conf', os.path.expanduser('~/.lsgprc')],
        help="path of configuration file",
    )
parser.add_argument("-v", "--verbose",
    action="store_true",
        help="florid proze output",
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

from tui import Main
main = Main()
main.run()

