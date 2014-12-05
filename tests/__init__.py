""" Python-Zimbra test suite
"""

import sys

# Py2-Compatibility

if sys.version < '3':

    from ConfigParser import ConfigParser

else:

    from configparser import ConfigParser


def get_config():

    parser = ConfigParser()

    parser.readfp(open('config.ini.dist'))
    parser.read('config.ini')

    return parser
