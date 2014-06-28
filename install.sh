
##############################
# Distribute Script for Vine #
##############################

# WARNING: the script is not mature.
# Read https://github.com/vine-comment/vine/blob/master/PREREQUISITE.md for more details.

install_pypackages()
{
    #######################
    # install pip section #
    #######################
    sudo pip install -U pip -i http://pypi.douban.com/simple

    if [ $? -ne 0 ]; then
        sudo apt-get install python-pip
    fi

    ######################
    # virtualenv section #
    ######################
    sudo pip install virtualenv
    virtualenv ~/vine
    ./activate.sh

    # NOTE: If you're using windows, please use Pillow installer from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/
    # (Pillow is a better maintained PIL lib.)
    items_pip="django-registration django-crispy-forms django-admin-bootstrapped django-haystack jieba Whoosh Pillow python-social-auth python-memcached django_akismet_comments elasticsearch pyelasticsearch django-avatar pytz pygeoip"

    for i in $items_pip; do
        pip install -i http://pypi.douban.com/simple $i
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
    cp config/gunicorn_start ~/vine/bin/
}

install_mac ()
{
    echo "NOTE: you should install JDK 1.7 first."
    echo "we will download brew(like apt-get) and install mongodb and elasticsearch."
    echo "it will take a long time, please wait."
    ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
    brew install mongodb
    brew install elasticsearch
    # consider mac section of installing openstack
    install_pypackages
}

install_ubuntu ()
{
    # TODO install mongodb etc.
    # TODO install elasticsearch: https://gist.github.com/aaronshaf/1190526
    echo "You should install elasticsearch by yourself."
    # sudo apt-get install mongodb
    # For IP database
    sudo apt-get install libgeoip-dev

    HOME=~
    install_pypackages

    ####################
    # gunicorn section #
    ####################
    pip install gunicorn
    cp gunicorn_start bin/.

    ######################
    # supervisor section #
    ######################
    echo "Installing and configuring supervisor..."
    sudo apt-get install supervisor

    sudo cat << EOF >/etc/supervisor/conf.d/vine.conf
[program:vine]
command = $HOME/vine/bin/gunicorn_start                                   ; Command to start app
user = root                                                               ; User to run as
stdout_logfile = $HOME/vine/logs/gunicorn_supervisor.log                  ; Where to write log messages
redirect_stderr = true
EOF
    # wtf.. eof

    mkdir -p $HOME/vine/logs
    touch $HOME/vine/logs/gunicorn_supervisor.log
    sudo supervisord

    sudo supervisorctl reread
    sudo supervisorctl update


    #################
    # nginx section #
    #################
    echo "Installing and configuring Nginx.."
    sudo apt-get install nginx
    cp config/vine.nginxconf /etc/nginx/sites-available/vine
    ln -s /etc/nginx/sites-available/vine /etc/nginx/sites-enabled/vine
    cp -r server/d1/static $HOME/vine/static
    sudo service nginx start
}

main()
{
    if [ "$(uname)" = "Darwin" ]; then
        echo "Installing on MAC.."
        install_mac
    elif [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
        distrib=`grep DISTRIB_ID /etc/*-release | awk -F= '{print $2}'`
        echo "Your distrib is $distrib"
        echo "Support Ubuntu now.."
        if [ $distrib = Ubuntu ]; then
            install_ubuntu
        fi
    else
        echo "Unsupport OS $(uname -s)"
    fi
}

main
