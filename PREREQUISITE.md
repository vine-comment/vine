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
* django-simple-captcha
* elasticsearch (for ubuntu: pyelasticsearch)
* django-avatar
   * if can't work, see https://github.com/jezdez/django-avatar/issues/53
   * Change PIL to Pillow,  Change x86_64 to i386 if you are installing it to a 32-bit machine

###apt-get install / download & setup
*   python-dev
*   memcached

   > Windows x64: check **http://www.couchbase.com/communities/q-and-a/memcached-x64-version-couchbase**

*   [elasticearch](https://github.com/elasticsearch/elasticsearch)
   *   you may need to install java first

     > Check: **https://github.com/geekben/deployment/blob/master/java_on_ubuntu.md**

-----
###Items should run.
*   Run a mail server to use account authentication.
   * sendmail, smtp.gmail, etc. 
   * `python -m smtpd -n -c DebuggingServer localhost:1025`
   * postfix for ubuntu

    > Check: **https://help.ubuntu.com/12.04/serverguide/postfix.html**

*   Memcached server
   * Linux: if your memcached server don't run automatically, try `./memcached -d -m 2048 -l 10.0.0.40 -p 11211`
   * Windows: download and run the binary.

*  elasticsearch server
   * `cd <elasticsearch home>`
   * `bin/elasticsearch &`

    > Check: **https://github.com/elasticsearch/elasticsearch**

###search engine
* django-haystack
* **[Elasticsearch](http://www.elasticsearch.org/overview/elkdownloads/)**
