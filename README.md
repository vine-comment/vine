vine
========

###a 3rd party comment system

* main languages: JavaScript, Python
* main framework: jquery, django

####DOING

* ie8-9 compatiable (jquery problems)
* accounts
* android front
* use redis
* comment as a tree(site->dir1->dir2->last_pathname)
* ajax pagination(dynamic)

####BUG-TRACKING

* https://github.com/ bugs... the script couldn't work via https. maybe we need a https scripts
* iframe in page will load this plugin, it may be an unwanted action
* timezone is not correct.. now it's utc. we should display it as viewers' time. Or it should be showed like youtube?
* jquery confict again.

####BUG-FIXED

* http://www.douban.com/ on method has no response | need to specify jquery version. if it's below 1.8, then we should use bind instead. Maybe we should use multiply iframe to avoid jquery collision.
* http://www.iciba.com/ zindex not working | set zindex to 2147483646 (MAX-1) because some framework may be error on MAX.
* some plugin(js) doesn't work when loading vine. Solution(?): http://api.jquery.com/jQuery.noConflict/ | using noConflict and load jquery locally solved this problem!

####DONE:

1. simple B/S demo
2. use iframe to avoid css collision
3. firefox/chrome basic testing
4. basic chrome extension
5. pagination
6. per url comment
7. IE10 compability

####TODO-FRONT:
1. ie(haven't got a good idea) plugin
2. firefox(try greasemonkey) plugins
3. android app development
4. ie basic testing
5. 3 directions to display the plugin
6. IOS front
7. improve chrome extension, and publish it

####TODO-END
1. mongodb storage
2. hadoop cluster
3. redis cache

####TODO-MULTI
1. accounts
2. reply to reply
3. notification
4. timeline
5. @
6. tag

####Research other 3rd party comment system
1. disqus
2. juvia
3. http://www.discourse.org/
4. http://www.livefyre.com/
5. jcomment
6. another Alternatives
7. http://ralsina.com.ar/stories/twitter-as-a-comment-engine.html 
8. social media integrate
