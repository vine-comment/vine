###django-nonrel
  > Check **http://django-mongodb-engine.readthedocs.org/en/latest/topics/setup.html** to install.

* django-nonrel
* djangotoolbox
* django-mongodb-engine

###pip install
* django-registration
* django-crispy-forms
* django-admin-bootstrapped
* django-haystack
* jieba
* Whoosh
* Pillow
* python-social-auth
* python-memcached

###apt-get / download & setup
* python-dev (apt-get install python-dev)
* memcached

-----
###Items should run.
* Run a mail server to use account authentication.
  * sendmail, smtp.gmail, etc. 
  * python -m smtpd -n -c DebuggingServer localhost:1025
* Memcached server
  * LINUX: `./memcached -d -m 2048 -l 10.0.0.40 -p 11211`
  * WINDOWS: run the binary.
