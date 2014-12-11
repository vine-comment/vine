#!/usr/bin/env python
#coding:utf8

import argparse
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d1.settings")

from vine_comment.models import Url, Comment

parser = argparse.ArgumentParser(description='UGC CRUD Client.')
parser.add_argument('-a', '--add', help='add comment', nargs=2, metavar=('url', 'comment'))
parser.add_argument('-r', '--rem', help='rem comment', nargs=2, metavar=('url', 'comment'))
parser.add_argument('-g', '--get', help='get comment', nargs=2, metavar=('url', 'comment'))
parser.add_argument('-m', '--mod', help='mod comment', nargs=2, metavar=('url', 'comment'))

cmds = ['add', 'rem', 'get', 'mod']
short_cmds = ['a', 'r', 'g', 'm']

class UGCManager(object):
    @staticmethod
    def add(url, comment):
        pass

    @staticmethod
    def rem(url, comment):
        pass

    @staticmethod
    def get(url, comment):
        pass

    @staticmethod
    def mod(url, comment):
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
        func = getattr(UGCManager, key)
        if len(args[key]) == 1:
            func(args[key][0])
        elif len(args[key]) == 2:
            func(args[key][0], args[key][1])

if __name__ == '__main__':
    main()


