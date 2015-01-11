#!/usr/bin/env python

import base64
import sys

p1 = ['e', 'd']

def usage():
    print 'usage: ', p1
    print 'sample: ./b64.py d \'aHR0cDovL3d3dy5iYWlkdS5jb20v\''
    print '        ./b64.py e \'http://www.baidu.com/\''

def main():
    if len(sys.argv) < 3:
        return usage()
    i = sys.argv[2]
    f = sys.argv[1]

    if f not in p1:
        usage()

    if 'e' == f:
        url_b64 = base64.b64encode(i, '+-')
        print url_b64
    if f == 'd':
        url = base64.b64decode(i, '+-')
        print url

if __name__ == '__main__':
    main()
