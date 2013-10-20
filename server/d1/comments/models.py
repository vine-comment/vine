from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    id = models.CharField(max_length=64)
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
    date = models.DateField()
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    desc = models.CharField(max_length=64)
    pass