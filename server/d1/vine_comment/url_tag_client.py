#!/usr/bin/env python
#coding:utf8

import argparse

parser = argparse.ArgumentParser(description='Test parser.')
parser.add_argument('--add', help='add url tag combination')
parser.add_argument('--rem', help='rem url tag combination')
parser.add_argument('--get', help='get url tag combination')
parser.add_argument('--mod', help='mod url tag combination')

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
    pass

if __name__ == '__main__':
    main()



