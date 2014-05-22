#!/bin/sh

##############################
# Install Script for Vine #
##############################

HOME=~
# WARNING: the script is not done.
# Read https://github.com/vine-comment/vine/blob/master/PREREQUISITE.md for more details.

sh prerequisite.sh

####################
# gunicorn section #
####################
pip install gunicorn
cp gunicorn_start bin/.

######################
# supervisor section #
######################
sudo apt-get install supervisor

(
sudo cat <<EOF
[program:vine]
command = $HOME/vine/bin/gunicorn_start                                   ; Command to start app
user = vine                                                               ; User to run as
stdout_logfile = $HOME/vine/logs/gunicorn_supervisor.log                  ; Where to write log messages
redirect_stderr = true 
EOF
) >/etc/supervisor/conf.d/vine.conf

mkdir -p /logs
touch $HOME/vine/logs/gunicorn_supervisor.log

sudo supervisorctl reread
sudo supervisorctl update
