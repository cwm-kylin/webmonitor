#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.conf import settings
from usermanagers.views.permission import PermissionVerify
from webmonitor.public import *

@login_required
@PermissionVerify()
def Home(request):
   #获取应用清单
   #排序
    MonitorAppInfoobj = MonitorAppInfo.objects.order_by('appname')

    if  request.method == 'GET' and 'appid' in request.GET:
        id=request.GET['appid']
        print U"首页----》",request.GET
        MonitorAppInforow=GetMonitorAppInfo(id)[0]
        print MonitorAppInforow,U"<=====MonitorAppInforow首页"

    return render_to_response('home.html',locals(),RequestContext(request))

def About(request):
   return render_to_response('about.html',locals(),RequestContext(request))





