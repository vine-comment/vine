#!/usr/bin/env python
#coding:utf8

import argparse
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d1.settings")

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from vine_comment.models import Url, Comment
from vine_comment.views import CommentView
from registration.backends.simple.views import RegistrationView


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

# User.objects.create_user(username, email, password)
# registration/backends/simple/views
#     def register(self, request, **cleaned_data):
#        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']

def get_author(user):
    if not user.is_authenticated():
        return None
    authors = Author.objects.filter(user=user)
    if authors:
        author = authors[0]
    else:
        author = Author.objects.create(
            user=user,
            time_added=datetime.datetime.utcnow().replace(tzinfo=utc)
            )
        author.save()
    return author

class AccountManager(object):
    @staticmethod
    def add(username, email, password):
        User.objects.create_user(username, email, password)
        new_user = authenticate(username=username, password=password)
        author = get_author(user)

    @staticmethod
    def rem():
        pass

class CommentUpManager(object):
    @staticmethod
    def add():
        pass

    @staticmethod
    def mod():
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


