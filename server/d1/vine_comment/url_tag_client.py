#!/usr/bin/env python
#coding:utf8

import argparse

parser = argparse.ArgumentParser(description='Url Tag Combination Client.')
parser.add_argument('-a', '--add', help='add url tag combination', nargs=2, metavar=('url', 'tag'))
parser.add_argument('-r', '--rem', help='rem url tag combination', nargs=2, metavar=('url', 'tag'))
parser.add_argument('-g', '--get', help='get url tag combination', nargs=2, metavar=('url', 'tag'))
parser.add_argument('-m', '--mod', help='mod url tag combination', nargs=2, metavar=('url', 'tag'))

class UrlTag(object):
    def add():
        print('add')
        pass
    def rem():
        print('rem')
        pass
    def get():
        print('get')
        pass
    def mod():
        print('mod')
        pass

def main():
    args = parser.parse_args()

if __name__ == '__main__':
    main()



