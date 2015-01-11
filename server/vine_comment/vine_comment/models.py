#coding:utf-8

from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import EmbeddedModelField, ListField
from django.utils.timezone import utc
from django.contrib.auth.signals import user_logged_out
import datetime

class TimeMixin(models.Model):
    time_modified = models.DateTimeField(blank=True, null=True)
    time_added = models.DateTimeField(
        default=datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    #time_added=datetime.datetime.utcnow().replace(tzinfo=utc)
    time_deleted = models.DateTimeField(blank=True, null=True)

    def modify(self):
        self.time_modified = datetime.datetime.utcnow().replace(tzinfo=utc)
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
    is_not_human = models.BooleanField(default=False) #trust at first time
    title = models.CharField(max_length=64, null=True)
    points = models.IntegerField(default=0)
    continuous_login = models.IntegerField(default=1)
    history_c_login = models.IntegerField(default=1)
    last_login = models.DateTimeField(blank=True, null=True)
    last_request = models.DateTimeField(blank=True,
        default=datetime.datetime.utcnow().replace(tzinfo=utc))
    comments_sum = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.user)

class Url(models.Model):
    url = models.URLField(max_length=2048)
    content = models.CharField(max_length=64)

    def __unicode__(self):
        return self.content

class CommentBoard(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True)
    url = models.URLField(max_length=2048, blank=True, null=True)

    def __unicode__(self):
        return self.title

class Tag(TimeMixin, models.Model):
    name = models.CharField(max_length=30)
    comments = ListField(models.ForeignKey('Comment'))
    urls = ListField(models.ForeignKey(Url))

class Comment(TimeMixin, models.Model):
    title = models.CharField(max_length=64)
    comment_str = models.CharField(max_length=128)
    #comment_img = models.ImageField(upload_to='comment_img/%Y/%m/%d', blank=True, null=True)
    url_b64 = models.CharField(max_length=100)#this is the name of this page's screenshot image
    desc = models.CharField(max_length=64, blank=True, null=True)
    comment_board = models.ForeignKey(CommentBoard)
    author_ip = models.IPAddressField(blank=True, null=True)
    # 在后面加入author的详细信息，分为匿名和实名
    author = models.ForeignKey(Author, blank=True, null=True)
    up_users = ListField(models.ForeignKey(User))
    down_users = ListField(models.ForeignKey(User))
    replies = ListField(EmbeddedModelField('Reply'))
    tags = ListField(EmbeddedModelField('Tag'))

    def __unicode__(self):
        return self.time_added.strftime("%Y-%m-%d %H:%M:%S") + ' ' + self.title + ' ' + self.comment_str

    @models.permalink
    def get_absolute_url(self):
        return ('comment-detail', [], {'id': self.id})

class Reply(TimeMixin, models.Model):
    comment = models.ForeignKey(Comment)
    reply_str = models.CharField(max_length=128)
    author_ip = models.IPAddressField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)

