from django.db import models

# Create your models here.
class Comment(models.Model):
    time = models.DateTimeField() #datetime.datetime
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    desc = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.title + ':' + self.content