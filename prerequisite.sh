#!/bin/sh

##############################
# Distribute Script for Vine #
##############################

# WARNING: the script is not done.
# Read https://github.com/vine-comment/vine/blob/master/PREREQUISITE.md for more details.

sudo -s

###############
# pip section #
###############

pip install -U pip -i http://pypi.douban.com/simple

if [ $? -ne 0 ]; then
  apt-get install python-pip
fi

items_pip=( django-registration django-crispy-forms django-admin-bootstrapped django-haystack jieba Whoosh Pillow python-social-auth python-memcached django_akismet_comments elasticsearch pyelasticsearch django-avatar )

alias p='pip install -i http://pypi.douban.com/simple'



for i in ${items_pip[@]}; do
p $i
done


# TODO:
# django-nonrel section
# apt-get / download & setup section


