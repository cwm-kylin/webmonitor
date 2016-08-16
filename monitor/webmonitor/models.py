# -*- coding: utf-8 -*-

from django.db import models

"""
=主机表
"""
class MonitorAppInfo(models.Model):
    id = models.AutoField(primary_key=True,max_length=6)
    appname =  models.CharField(max_length=40,unique=True)
    url = models.CharField(max_length=100)
    isp = models.CharField(max_length=10)
    alarmtype = models.CharField(max_length=8)
    alarmconditions = models.CharField(max_length=30)

"""
=监控结果表
"""
class MonitorData(models.Model):
    id = models.AutoField(primary_key=True,max_length=6)
    FID = models.SmallIntegerField()
    NAMELOOKUP_TIME =  models.FloatField()
    CONNECT_TIME =  models.FloatField()
    PRETRANSFER_TIME =  models.FloatField()
    STARTTRANSFER_TIME =  models.FloatField()
    TOTAL_TIME =  models.FloatField()
    HTTP_CODE =  models.CharField(max_length=100)
    SIZE_DOWNLOAD =  models.FloatField()
    HEADER_SIZE =  models.SmallIntegerField()
    REQUEST_SIZE =  models.SmallIntegerField()
    CONTENT_LENGTH_DOWNLOAD=models.FloatField()
    SPEED_DOWNLOAD=models.FloatField()
    DATETIME=models.IntegerField()
    MARK=models.CharField(max_length=1)

