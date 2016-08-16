# -*- coding: utf-8 -*-

import string,re,os
import time,datetime
import logging


from webmonitor.models import MonitorAppInfo,MonitorData
from webmonitor.config import *
from decimal import Decimal
from django.conf import settings

#初始化日志对象
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    filename=os.path.dirname(os.path.realpath(__file__))+'/syslog.log',
                    filemode='a')






"""
=根据ID获取应用名称
-GetAppName(应用ID)
"""
def GetAppName(_id):
    return MonitorAppInfo.objects.values('appname').get(id=_id)


"""
=获取当前应用数据中心ID清单
-GetAppIDCId(应用ID)
"""
def GetAppIDCId(_id):
    from django.db import connection
    ID_list=[]
    try:
        cursor = connection.cursor()
        if _id==None:
            cursor.execute("select id from webmonitor_monitorappinfo")
        else:
            cursor.execute("select id from webmonitor_monitorappinfo where url in (select url from webmonitor_monitorappinfo where id='%d')"%(int(_id)))
        for row in cursor.fetchall():
            ID_list.append(row[0])
        return ID_list
    except Exception,e:
        logging.error('select database error!'+str(e))
        return


"""
=获取当前应用数据中心名称清单
-GetAppIDCName(应用ID)
"""
def GetAppIDCName(_id):
    from django.db import connection
    ID_list=[]
    try:
        cursor = connection.cursor()
        if _id==None:
            cursor.execute("select idc,appname from webmonitor_monitorappinfo")
        else:
            cursor.execute("select idc,appname from webmonitor_hostinfo where url in (select url from webmonitor_monitorappinfo where id='%d')"%(int(_id)))
        for row in cursor.fetchall():
            ID_list.append(row)
        return ID_list
    except Exception,e:
        logging.error('select database error!'+str(e))
        return


"""
=获取应用表数据
-GetMonitorAppInfo(应用ID)
"""
def GetMonitorAppInfo(_id):
        return MonitorAppInfo.objects.filter(id=_id)

"""
=日期转时间戳
-time2stamp(日期＋时间)
"""
def time2stamp(_datetime):
        return int(time.mktime(time.strptime(_datetime,'%Y-%m-%d %H:%M:%S')))

"""
=时间戳转日期
-stamp2time(时间戳)
"""
def stamp2time(_stamp):
        stamp=time.localtime(_stamp)
        return time.strftime("%Y-%m-%d %H:%M:%S", stamp)





"""
=获取URL域名
-GetURLdomain(url)
-返回URL域名,例如:www.baidu.com
"""
def GetURLdomain(url):
    xurl=""
    if url[:7]=="http://":
        xurl=url[7:]
    else:
        xurl=url
    return string.split(xurl,'/')[0]


"""
=获取URL路径部分
-GetURLpath(url)
-返回URL路径,例如:/pub/content/1/364563.html
"""
def GetURLdopath(url):
    xurl=""
    if url[:7]=="http://":
        xurl=url[8:]
    else:
        xurl=url
    return xurl[xurl.find('/'):]


"""
=获取监控URL ID
-getID(url)
"""
def getID(url):
    URL=url
    HID=[]
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("select id from webmonitor_monitorappinfo where URL='%s'"%(URL))
    for row in cursor.fetchall():
        HID.append(row[0])
    connection.close()
    return HID



