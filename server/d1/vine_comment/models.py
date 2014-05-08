#coding:utf-8

from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import EmbeddedModelField, ListField
import datetime

class TimeMixin(models.Model):
    time_modified = models.DateTimeField(blank=True, null=True)
    time_added = models.DateTimeField()
    time_deleted = models.DateTimeField(blank=True, null=True)

    def modify(self):
        self.time_modified = datetime.datetime.now()
        super(TimeMixin, self).modify()
    
    def __unicode__(self):
        return str(self.time_added)

    class Meta:
        abstract = True

class CountMixin(models.Model):
    count_viewed = models.IntegerField()
    count_modified = models.IntegerField()

    def view(self):
        self.count_viewd += 1
        super(CountMixin, self).view()

class RateMixin(models.Model):
    rate_average = models.IntegerField()
    rate_count = models.IntegerField()

    def rate(self):
        self.rate_average
        super(RateMixin, self).rate()

# Create your models here.
class Author(TimeMixin, models.Model):
    """
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
    """
    picture = models.ImageField(upload_to='head_sculpture', blank=True, null=True)
    
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.user.name

class Url(models.Model):
    content = models.CharField(max_length=64)
    url = models.URLField(max_length=2048)

    def __unicode__(self):
        return self.content

class CommentBoard(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True)
    url = models.URLField(max_length=2048, blank=True, null=True)
    
    def __unicode__(self):
        return self.title

class Comment(TimeMixin, models.Model):
    title = models.CharField(max_length=64)
    comment_str = models.CharField(max_length=128)
    desc = models.CharField(max_length=64, blank=True, null=True)
    comment_board = models.ForeignKey(CommentBoard)
    author_ip = models.IPAddressField(blank=True, null=True)
    # 在后面加入author的详细信息，分为匿名和实名
    author = models.ForeignKey(Author, blank=True, null=True)
    up_users = ListField(models.ForeignKey(User))
    down_users = ListField(models.ForeignKey(User))
    replies = ListField(EmbeddedModelField('Reply'))
    tags = ListField(models.CharField(max_length=128))

    def __unicode__(self):
        return self.time_added.strftime("%Y-%m-%d %H:%M:%S") + self.title + ' ' + self.comment_str

    @models.permalink
    def get_absolute_url(self):
        return ('comment-detail', [], {'id': self.id})

class Reply(TimeMixin, models.Model):
    comment = models.ForeignKey(Comment)
    reply_str = models.CharField(max_length=128)
    author_ip = models.IPAddressField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)

