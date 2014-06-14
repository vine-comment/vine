#!/bin/sh

##############################
# Distribute Script for Vine #
##############################

# WARNING: the script is not done.
# Read https://github.com/vine-comment/vine/blob/master/PREREQUISITE.md for more details.


###############
# pip section #
###############

sudo pip install -U pip -i http://pypi.douban.com/simple

if [ $? -ne 0 ]; then
  sudo apt-get install python-pip
fi

######################
# virtualenv section #
######################
sudo pip install virtualenv
cd ..
virtualenv ~/vine
source ~/vine/bin/activate

# NOTE: If you're using windows, please use Pillow installer from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/
# (Pillow is a better maintained PIL lib.)
items_pip=( django-registration django-crispy-forms django-admin-bootstrapped django-haystack jieba Whoosh Pillow python-social-auth python-memcached django_akismet_comments elasticsearch pyelasticsearch django-avatar )

alias p='sudo pip install -i http://pypi.douban.com/simple'

for i in ${items_pip[@]}; do
  p $i
done


#########################
# django-nonrel section #
#########################
pip install git+https://github.com/django-nonrel/django@nonrel-1.5
pip install git+https://github.com/django-nonrel/djangotoolbox
pip install git+https://github.com/django-nonrel/mongodb-engine

####################
# gunicorn section #
####################
pip install gunicorn
cp gunicorn_start ~/vine/bin/


# TODO:
# apt-get / download & setup section


