from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)

    def __str__(self):
        return '%s' %(self.username)

class Keyword(models.Model):
    keyword = models.CharField(max_length=100)
    date =  models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return '%s' %(self.keyword)

class SearchedDate(models.Model):
   
    startDate =  models.CharField(max_length=100)
    endDate = models.CharField(max_length=100)

    def __str__(self):
        return '%s' %(self.startDate)        