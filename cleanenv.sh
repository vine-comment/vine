
#######################
# install pip section #
#######################
sudo pip install -U pip -i http://pypi.douban.com/simple

if [ $? -ne 0 ]; then
    sudo apt-get install python-pip
fi

deactivate

items_pip="django-registration django-crispy-forms django-admin-bootstrapped django-haystack jieba Whoosh Pillow python-social-auth python-memcached django_akismet_comments elasticsearch pyelasticsearch django-avatar pytz pygeoip PIL"

for i in $items_pip; do
    pip uninstall $i
done


#########################
# django-nonrel section #
#########################
pip uninstall Django
pip uninstall djangotoolbox
pip uninstall mongodb-engine

####################
# gunicorn section #
####################
pip uninstall gunicorn
