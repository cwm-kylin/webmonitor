# -*- coding: utf-8 -*-
import os,sys
import time
import sys
import pycurl
import rrdtool
import string
import MySQLdb
from  config import *
import logging

class UpdateRRD():
    #初始化    
    def __init__(self):
        #初始化日志对象
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    filename=os.path.dirname(os.path.realpath(__file__))+'/syslog.log',
                    filemode='a')
        
        #连接数据
        try:
            self.conn =   MySQLdb.Connection(DBHOST, DBUSER, DBPASSWORD, DBNAME)
            self.cursor =  self.conn.cursor(MySQLdb.cursors.DictCursor)
        except Exception,e:
            logging.error('connect database error!'+str(e))
            return
        
        self.rrdfiletype=['time','download','unavailable']

    #虚构方法
    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception,e:
            logging.debug('__del__ object error!'+str(e))

    #更新rrd文件
    def updateRRD(self,rowobj):
        if str(rowobj["HTTP_CODE"])=="200":
            unavailablevalue=0
        else:
            unavailablevalue=1
        FID=rowobj["FID"]
        
        time_rrdpath=RRDPATH+'/'+str(self.getURL(FID))+'/'+str(FID)+'_'+str(self.rrdfiletype[0])+'.rrd'
        download_rrdpath=RRDPATH+'/'+str(self.getURL(FID))+'/'+str(FID)+'_'+str(self.rrdfiletype[1])+'.rrd'
        unavailable_rrdpath=RRDPATH+'/'+str(self.getURL(FID))+'/'+str(FID)+'_'+str(self.rrdfiletype[2])+'.rrd'

        try:
            rrdtool.updatev(time_rrdpath,'%s:%s:%s:%s:%s:%s' % (str(rowobj["DATETIME"]),str(rowobj["NAMELOOKUP_TIME"]),str(rowobj["CONNECT_TIME"]),str(rowobj["PRETRANSFER_TIME"]),str(rowobj["STARTTRANSFER_TIME"]),str(rowobj["TOTAL_TIME"])))
            rrdtool.updatev(download_rrdpath,'%s:%s' % (str(rowobj["DATETIME"]),str(rowobj["SPEED_DOWNLOAD"])))
            rrdtool.updatev(unavailable_rrdpath,'%s:%s' % (str(rowobj["DATETIME"]),str(unavailablevalue)))
            self.setMARK(rowobj["id"])
        except Exception,e:
            logging.error('Update rrd error:'+str(e))
        

    #更新已标志记录
    def setMARK(self,_id):
        try:
            self.cursor.execute("update webmonitor_monitordata set MARK='1' where id='%s'"%(_id))
            self.conn.commit()
        except Exception,e:
            logging.error('SetMark datebase  error:'+str(e))

    #获取未标志的新记录
    def getNewdata(self):
        try:
            self.cursor.execute("select id,FID,NAMELOOKUP_TIME,CONNECT_TIME,PRETRANSFER_TIME,STARTTRANSFER_TIME,TOTAL_TIME,HTTP_CODE,SPEED_DOWNLOAD,DATETIME from webmonitor_monitordata where MARK='0'")
            for row in self.cursor.fetchall():
                self.updateRRD(row)
        except Exception,e:
            logging.error('Get new database  error:'+str(e))


    #获取域名
    def getURL(self,_id):
        try:
            self.cursor.execute("select url from webmonitor_monitorappinfo where id='%s'"%(_id))
            return self.GetURLdomain(self.cursor.fetchall()[0]["url"])
        except Exception,e:
            logging.error('Get FID URL  error:'+str(e))

        
    #获取URL域名
    def GetURLdomain(self,url):
        xurl=""
        if url[:7]=="http://":
            xurl=url[7:]
        else:
            xurl=url
        return string.split(xurl,'/')[0]

if __name__ == '__main__':
    app=UpdateRRD()
    app.getNewdata()