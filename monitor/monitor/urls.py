# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from monitor.views import Home,About

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    #admin后台登陆
    url(r'^admin/', include(admin.site.urls)),
    #用户权限管理
    url(r'^$',Home),
    url(r'^about/$',About),

    url(r'^accounts/',include('usermanagers.urls')),
    #业务线监控
    url(r'^webmonitor/',include('webmonitor.urls')),


    #static
   # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,}),

)
