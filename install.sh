#!/bin/sh

##############################
# Install Script for Vine #
##############################

# WARNING: the script is not done.
# Read https://github.com/vine-comment/vine/blob/master/PREREQUISITE.md for more details.

sh prerequisite.sh

####################
# gunicorn section #
####################
pip install gunicorn
cp gunicorn_start bin/.


# TODO:
# apt-get / download & setup section


