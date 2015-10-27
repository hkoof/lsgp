import sys
import os.path
import configparser
from collections import OrderedDict


class Config(configparser.ConfigParser):
    def __init__(self, filename=None):
        super().__init__(dict_type=OrderedDict)
        self['monitor'] = {
            'url': 'ldapi:///',
            'ssl': 'no',
            'auth': 'SIMPLE',
            'binddn': '',
            'password': '',
        }
        if filename is not None:
            self.read(filename)

    def print(self):
        self.write(sys.stdout)
    

def main():
    config = Config(os.path.expanduser('~/.ldapparc'))
    config.print()

if __name__ == "__main__":
    main()
