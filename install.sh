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
}

install_mac ()
{
    echo "we will download brew(like apt-get on ubuntu) and install mongodb."
    echo "it will take a long time, please wait."
    ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
    brew install mongodb
    # consider mac section of installing openstack
    install_pypackages
}

install_ubuntu ()
{
    # TODO install mongodb etc.

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
    sudo apt-get install supervisor

    sudo cat << EOF >/etc/supervisor/conf.d/vine.conf
    [program:vine]
    command = $HOME/vine/bin/gunicorn_start                                   ; Command to start app
    user = vine                                                               ; User to run as
    stdout_logfile = $HOME/vine/logs/gunicorn_supervisor.log                  ; Where to write log messages
    redirect_stderr = true
EOF
    # wtf.. eof

    mkdir -p /logs
    touch $HOME/vine/logs/gunicorn_supervisor.log

    sudo supervisorctl reread
    sudo supervisorctl update


    #################
    # nginx section #
    #################
    sudo apt-get install nginx
    sudo service nginx start
}

main()
{
    if [ "$(uname)" == "Darwin" ]; then
        install_mac
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        install_ubuntu
    else
        echo "Unsupport OS $(uname -s)"
    fi
}

main
