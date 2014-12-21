#!/usr/bin/env python
#coding:utf8

import datetime
import argparse
import sys
sys.path.append('../')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d1.settings")

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.timezone import utc

from vine_comment.models import Url, Comment, Author
from vine_comment.views import CommentView
from registration.backends.simple.views import RegistrationView


parser = argparse.ArgumentParser(description='Author test client.')
parser.add_argument('-a', '--add', help='add author', nargs=3, metavar=('username', 'email', 'password'))
parser.add_argument('-af', '--addfile', help='add author batch from file', nargs=1, metavar=('fname'))

cmds = ['add', 'addfile', 'rem', 'get', 'mod']
short_cmds = ['a', 'af', 'r', 'g', 'm']


def get_author(user):
    if not user.is_authenticated():
        return None
    authors = Author.objects.filter(user=user)
    if authors:
        author = authors[0]
        print "Author exists!"
    else:
        author = Author.objects.create(
            user=user,
            time_added=datetime.datetime.utcnow().replace(tzinfo=utc)
            )
        author.save()
    return author

class AuthorManager(object):
    @staticmethod
    def add(username, email, password):
        user = User.objects.filter(username=username)
        if not user:
            User.objects.create_user(username, email, password)
        else:
            print "User exists!"
        user = authenticate(username=username, password=password)
        author = get_author(user)
        print author

    @staticmethod
    def rem():
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
        func = getattr(AuthorManager, key)
        if len(args[key]) == 1:
            func(args[key][0])
        elif len(args[key]) == 2:
            func(args[key][0], args[key][1])
        elif len(args[key]) == 3:
            func(args[key][0], args[key][1], args[key][2])

if __name__ == '__main__':
    main()


