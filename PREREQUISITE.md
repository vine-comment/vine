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
* django_akismet_comments

###apt-get install / download & setup
* python-dev
* memcached

  > Windows x64: check **http://www.couchbase.com/communities/q-and-a/memcached-x64-version-couchbase**

-----
###Items should run.
* Run a mail server to use account authentication.
  * sendmail, smtp.gmail, etc. 
  * python -m smtpd -n -c DebuggingServer localhost:1025
* Memcached server
  * Linux: if your memcached server don't run automatically, try `./memcached -d -m 2048 -l 10.0.0.40 -p 11211`
  * Windows: download and run the binary.
