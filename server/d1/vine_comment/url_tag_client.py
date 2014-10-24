#!/usr/bin/env python
#coding:utf8

import argparse
from models import UrlTag


parser = argparse.ArgumentParser(description='Url Tag Combination Client.')
parser.add_argument('-a', '--add', help='add url tag combination', nargs=2, metavar=('url', 'tag'))
parser.add_argument('-r', '--rem', help='rem url tag combination', nargs=2, metavar=('url', 'tag'))
parser.add_argument('-g', '--get', help='get url tag combination', nargs=2, metavar=('url', 'tag'))
parser.add_argument('-m', '--mod', help='mod url tag combination', nargs=2, metavar=('url', 'tag'))

cmds = ['add', 'rem', 'get', 'mod']
short_cmds = ['a', 'r', 'g', 'm']

class UrlTag(object):
    @staticmethod
    def add(*args, **kwargs):
        pass

    @staticmethod
    def rem(*args, **kwargs):
        pass

    @staticmethod
    def get(*args, **kwargs):
        pass

    @staticmethod
    def mod(*args, **kwargs):
        pass

def main():
    args = vars(parser.parse_args())
    print("args: " + str(args))

    for key in args:
        if args[key] is None:
            continue
        print('calling '+key)
        func = getattr(UrlTag, key)
        result = func(args[key])

if __name__ == '__main__':
    main()



