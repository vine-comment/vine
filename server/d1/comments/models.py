from django.db import models
from django.contrib.auth.models import User
import datetime

class TimeMixin(models.Model):
    time_modified = models.DateTimeField()
    time_added = models.DateTimeField()

    def save(self):
        self.time_modified = datetime.datetime.now()
        super(TimeMixin, self).save()

# Create your models here.
class Author(models.Model):
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

class Comment(models.Model):
    time = models.DateTimeField() #datetime.datetime
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    desc = models.CharField(max_length=64)
    

    pass

class Url(models.Model):
    pass

class CommentBoard(models.Model):
    url = models.ForeignKey(Url)
    comments = models.ForeignKey(Comment)
