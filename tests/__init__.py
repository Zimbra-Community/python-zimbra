""" Python-Zimbra test suite
"""

from ConfigParser import ConfigParser


def get_config():

    parser = ConfigParser()

    parser.readfp(open('config.ini.dist'))
    parser.read('config.ini')

    return parser