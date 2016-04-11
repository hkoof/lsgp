import sys
import os.path
import configparser
from collections import OrderedDict


class Config(configparser.ConfigParser):
    def __init__(self, files=None):
        super().__init__(dict_type=OrderedDict)
        self['monitor'] = {
            'url': 'ldapi:///',
            'ssl': 'no',
            'auth': 'SIMPLE',
            'binddn': '',
            'password': '',
        }
        if files is not None:
            if isinstance(files, str):
                files = [files]
            conffilepresent = False
            for f in files:
                if os.path.exists(f):
                    self.read(files)
                    break
            else:
                raise FileNotFoundError(files)

    def print(self):
        self.write(sys.stdout)
