
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

echo "Use 'source ~/vine/bin/activate' to get into the virtualenv!!!"
