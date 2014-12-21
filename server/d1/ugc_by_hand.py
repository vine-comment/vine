#!/usr/bin/env python
#coding:utf8

import argparse
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d1.settings")

from vine_comment.models import Url, Comment
from vine_comment.views import CommentView

parser = argparse.ArgumentParser(description='UGC CRUD Client.')
parser.add_argument('-a', '--add', help='add comment', nargs=2, metavar=('url', 'comment'))
parser.add_argument('-af', '--addfile', help='add comment batch from file', nargs=2, metavar=('url', 'fname'))

cmds = ['add', 'addfile', 'rem', 'get', 'mod']
short_cmds = ['a', 'aj', 'r', 'g', 'm']

class CommentManager(object):
    @staticmethod
    def add(url='http://www.default-test.com/', comment='default-test-comment'):
        CommentView._post_comment(url, comment, author_ip="1.2.3.4", user=None)

    @staticmethod
    def addfile(url, fname):
        with open(fname) as f:
            for line in f:
                CommentView._post_comment(url, line, author_ip="1.2.3.4", user=None)

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
        func = getattr(CommentManager, key)
        if len(args[key]) == 1:
            func(args[key][0])
        elif len(args[key]) == 2:
            func(args[key][0], args[key][1])

if __name__ == '__main__':
    main()


