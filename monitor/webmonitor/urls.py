#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'kylin'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('webmonitor',
    #url(r'^index/','views.index',name='monitordatainfourl'),
    url(r'^list/','views.ListApp',name='listmonitorurl'),
    url(r'^add/','views.AddApp',name='monitoraddurl'),
    url(r'^edit/(?P<ID>\d+)/$','views.EditApp',name='monitorediturl'),
    url(r'^del/(?P<ID>\d+)/$','views.DelApp',name='monitordelurl'),
    url(r'monitordata/','views.monitordata',name='monitordataurl'),
    url(r'^monitorlist/','views.monitorlist',name='monitorlisturl'),

)


