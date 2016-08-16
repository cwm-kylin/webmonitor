# -*- coding: utf-8 -*-
import os,time
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from monitor.common.CommonPaginator import SelfPaginator
from usermanagers.views.permission import PermissionVerify
from webmonitor.forms import MonitorinfoForm,EditMonitorinfoForm
from webmonitor.models import MonitorAppInfo,MonitorData
from public import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage


"""
=业务线显示列表
"""
@login_required
@PermissionVerify()
def ListApp(request):
    mList = MonitorAppInfo.objects.all()
    #print mList,type(mList)
    #print mList.values()

    #分页功能
    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('webmonitor/webmonitor.list.html',kwvars,RequestContext(request))




"""
=业务线添加，
"""
@login_required
@PermissionVerify()
def AddApp(request):
    if request.method=='POST':
        form =  MonitorinfoForm(request.POST)
        if form.is_valid():
            data = form.clean()
            print "data===>>",data
            URL=request.POST['url']
            HostDomain=GetURLdomain(URL)
            print "HostDomain----》",HostDomain
            form.save()
            print "URL IS ---->",URL


        return HttpResponseRedirect(reverse('listmonitorurl'))
    else:
        form =  MonitorinfoForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('webmonitor/webmonitor.add.html',kwvars,RequestContext(request))


"""
=业务线修改
"""

@login_required
@PermissionVerify()
def EditApp(request,ID):
    obj = MonitorAppInfo.objects.get(id = ID)
    #print MonitorAppInfo.objects.values("isp"),"<========="
    print "obj--===-->",obj
    OLD_URL=MonitorAppInfo.objects.values("url").filter(id=ID)
    for i in OLD_URL:
       Old_URL=i['url']
    print "Old_UR---->>>",Old_URL,type(Old_URL)
    if request.method=='POST':
        form = EditMonitorinfoForm(request.POST,instance=obj)
        if form.is_valid():
            data = form.clean()
            print data,"<======"
            form.save()
            URL=request.POST['url']
            New_HostDomain=GetURLdomain(URL)
            ##删除RRD目录从新添加RRD目录
            Old_HostDomain=str(GetURLdomain(Old_URL))
            print 'Old_HostDomain IS:---->',Old_HostDomain

        return HttpResponseRedirect(reverse('listmonitorurl'))
    else:
        form = EditMonitorinfoForm(instance=obj)

    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }

    return render_to_response('webmonitor/webmonitor.edit.html',kwvars,RequestContext(request))


"""
=业务线删除
"""
@login_required
@PermissionVerify()
def DelApp(request,ID):
    MonitorAppInfo.objects.filter(id = ID).delete()
    MonitorData.objects.filter(FID=ID).delete()

    return HttpResponseRedirect(reverse('listmonitorurl'))




"""
=监控列表上版页面
"""
@login_required
@PermissionVerify()
def monitordata(request):
    #获取应用清单

    if  request.method == 'GET'  and 'appid' in request.GET and 'StartTime' in request.GET and 'EndTime' in request.GET:
        MonitorAppInfoobj = MonitorAppInfo.objects.order_by('appname')
        print u"前端页面提交所有信息123==----==>",request.GET

        id=request.GET['appid']
        print id
        MonitorAppInforow=GetMonitorAppInfo(id)[0]
        Appdomain=str(GetURLdomain(url=MonitorAppInforow.url))
        print "MonitorAppInforow is:===>",MonitorAppInforow
        print "Appdomain is : ====>",Appdomain
        StartTime= request.GET['StartTime']
        EndTime= request.GET['EndTime']
        MonitorAppInforow=MonitorAppInforow

        print 'MonitorAppInforow before=======',MonitorAppInforow
        if not 'StartTime' in request.GET or request.GET['StartTime']=="":
            StartTime=int(str(time.time()).split('.')[0])-86400*3
            EndTime=int(str(time.time()).split('.')[0])
            kylin_tag="0"
            print "MonitorAppInforow.id,MonitorAppInforow.url,MonitorAppInforow.appname is>>>",MonitorAppInforow.id,MonitorAppInforow.url,MonitorAppInforow.appname
            #Graphrrd_normal(_id=MonitorAppInforow.id,url=MonitorAppInforow.url,appname=MonitorAppInforow.appname)    #custom graph rrd

        else:
            print u"前端页面提交所有信息2222==----==>",request.GET
            #自定义时间查询及生成rrd图表
            StartTime=time2stamp(request.GET['StartTime'])
            EndTime=time2stamp(request.GET['EndTime'])
            print 'StartTime,EndTime =======>>IS:',StartTime,EndTime
            kylin_tag="1"
            #graphrrd user defind

            #Graphrrd_custom(_id=MonitorAppInforow.id,url=MonitorAppInforow.url,appname=MonitorAppInforow.appname)    #custom graph rrd
        kwvars = {
        'request':request,
        'ID':id,
        'StartTime':StartTime,
        'EndTime':EndTime,
        'MonitorAppInfoobj':MonitorAppInfoobj,
        'MonitorAppInfo':MonitorAppInfo,
        'Appdomain':Appdomain,
        }


        return render_to_response('webmonitor/webmonitordatainfo.html',kwvars,RequestContext(request))

    else:
        return render_to_response('webmonitor/webmonitordatainfo.html',{},RequestContext(request))


"""
=监控列表下版页面
"""
@login_required
@PermissionVerify()
def monitorlist(request):
    #获取应用清单
    print u"前端页面提交所有信息345==----==>",request.GET
    if  request.method == 'GET'  and 'appid' in request.GET and 'StartTime' in request.GET and 'EndTime' in request.GET:

        id=request.GET['appid']
        print id,"<<<=====id"
        StartTime= request.GET['StartTime']
        EndTime= request.GET['EndTime']

        #分页功能
        contact_list = MonitorData.objects.filter(FID=id, DATETIME__gte=StartTime,DATETIME__lte=EndTime).order_by("-DATETIME")
        paginator = Paginator(contact_list, 10)
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            contacts = paginator.page(page)
        except (EmptyPage, InvalidPage):
            contacts = paginator.page(paginator.num_pages)


        kwvars = {
        'contacts':contacts,
        'request':request,
        'ID':id,
        'StartTime':StartTime,
        'EndTime':EndTime,

        }


        return render_to_response('webmonitor/webmonitordatainfolist.html',kwvars,RequestContext(request))

    else:
        return render_to_response('webmonitor/webmonitordatainfolist.html',{},RequestContext(request))