from django.db import models
from django.contrib.auth.models import User
import datetime

class TimeMixin(object):
    time_modified = models.DateTimeField()
    time_added = models.DateTimeField()
    time_deleted = models.DateTimeField()

    def modify(self):
        self.time_modified = datetime.datetime.now()
        super(TimeMixin, self).modify()

class CountMixin(object):
    count_viewed = models.IntegerField()
    count_modified = models.IntegerField()

    def view(self):
        self.count_viewd += 1
        super(CountMixin, self).view()

class RateMixin(object):
    rate_average = models.IntegerField()
    rate_count = models.IntegerField()

    def rate(self):
        self.rate_average
        super(RateMixin, self).rate()
        pass

# Create your models here.
class Author(TimeMixin, models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.name

class Comment(models.Model):
    time = models.DateTimeField() #datetime.datetime
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    desc = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.title

class Url(models.Model):
    content = models.CharField(max_length=64)
    url = models.CharField(max_length=2048)
    
    def __unicode__(self):
        return self.content

class CommentBoard(models.Model):
    title = models.CharField(max_length=64)
    url = models.ForeignKey(Url)
    comments = models.ForeignKey(Comment)
    
    def __unicode(self):
        return self.title
