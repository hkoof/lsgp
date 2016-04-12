#!/usr/env/bin python

if __name__ != "__main__":
    raise ImportError("Program not importable.")

import sys
import os.path
import argparse
import logging
from logging.handlers import SysLogHandler

import prog
import ldapper
from config import Config, ConfigError


#### Command line parsing
#
parser = argparse.ArgumentParser(
        prog=prog.name,
        description=prog.description,
    )
parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s {}'.format(prog.version),
    )
parser.add_argument(
        "-c", "--config",
        default=['/etc/lsgp.conf', os.path.expanduser('~/.lsgprc')],
        help="path of configuration file",
    )
parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="florid proze logging",
    )
parser.add_argument(
        "--print-config", action='store_true',
        help="print configuration to standard output and exit",
    )
args = parser.parse_args()

conf = Config(args.config)
monitorconf = conf['monitor']

if args.print_config:
    conf.write(sys.stdout)
    sys.exit(0)

log = logging.getLogger(prog.name)
logconf = conf['logging']
loglevel = logconf.get('level')
logfile = logconf.get('file')
logsyslog = logconf.getboolean('syslog')

if loglevel == 'critical': loglevel = logging.CRITICAL
elif loglevel == 'error': loglevel = logging.ERROR
elif loglevel == 'warning': loglevel = logging.WARNING
elif loglevel == 'info': loglevel = logging.INFO
elif loglevel == 'debug': loglevel = logging.DEBUG
else: raise ConfigError("invalid loglevel '{}'".format(loglevel))
log.setLevel(loglevel)

if logfile:
    log_2file = logging.FileHandler(logfile) 
    log_2file.setLevel(loglevel)
    log_2file.setFormatter(logging.Formatter('%(asctime)s %(name)s: %(levelname)s %(message)s'))
    log.addHandler(log_2file)

if logsyslog:
    log_2syslog = SysLogHandler(address='/dev/log')
    log_2syslog.setLevel(loglevel)
    log_2syslog.setFormatter(logging.Formatter('%(name)s: %(levelname)s %(message)s'))
    log.addHandler(log_2syslog)

# LDAP connection for cn=monitor
cn_monitor = ldapper.Connection(conf['monitor'])
cn_monitor.open(None)

from tui import Main
main = Main(cn_monitor)
main.run()

