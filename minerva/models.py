from django.db import models
import django.utils.timezone as timezone
# Create your models here.

class Build(models.Model):
    gmt_create = models.DateTimeField('保存日期',default=timezone.now)
    gmt_modify = models.DateTimeField('最后修改日期',auto_now=True)
    creator = models.CharField(max_length=20, null=True, blank=True)
    modifier = models.CharField(max_length=20, null=True, blank=True)
    image = models.CharField(max_length=100)
    app_name = models.CharField(max_length=20)
    commit = models.CharField(max_length=1000, null=True,blank=True)

class App(models.Model):
    app_name = models.CharField(max_length=20)