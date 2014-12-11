#!/usr/bin/env python
#coding:utf8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d1.settings")

from vine_comment.models import Url, Tag, Comment
import argparse

parser = argparse.ArgumentParser(description='UGC CRUD Client.')
parser.add_argument('-a', '--add', help='add comment', nargs=2, metavar=('url', 'tag'))
parser.add_argument('-r', '--rem', help='rem comment', nargs=2, metavar=('url', 'tag'))
parser.add_argument('-g', '--get', help='get comment', nargs=2, metavar=('url', 'tag'))
parser.add_argument('-m', '--mod', help='mod comment', nargs=2, metavar=('url', 'tag'))

cmds = ['add', 'rem', 'get', 'mod', 'gett', 'getu', 'addjson']
short_cmds = ['a', 'r', 'g', 'm', 'gt', 'gu', 'aj']

class TagManager(object):
    @staticmethod
    def add(url, tag):
        pass

    @staticmethod
    def rem(url, tag):
        pass

    @staticmethod
    def get(url, tag):
        pass

    @staticmethod
    def mod(url):
        pass

def main():
    exist_arg = False
    args = vars(parser.parse_args())

    for key in args:
        if args[key] is not None:
            exist_arg = True

    if exist_arg is False:
        parser.print_help()
        return

    print("args: " + str(args))

    for key in args:
        if args[key] is None:
            continue
        print(key+' '+str(args[key]))
        func = getattr(TagManager, key)
        if len(args[key]) == 1:
            func(args[key][0])
        elif len(args[key]) == 2:
            func(args[key][0], args[key][1])

if __name__ == '__main__':
    main()


