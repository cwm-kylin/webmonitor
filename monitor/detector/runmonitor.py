# -*- coding: utf-8 -*-
import os,sys
import time
import sys
import pycurl
import string
import MySQLdb
from  config import *
import logging
from decimal import Decimal
import weixin



class Runmonitor():

    #构造方法
    def __init__(self):

        #初始化日志对象
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    filename=os.path.dirname(os.path.realpath(__file__))+'/syslog.log',
                    filemode='a')
        
        #连接数据
        try:
            self.conn =   MySQLdb.Connection(DBHOST, DBUSER, DBPASSWORD, DBNAME)
            self.cursor =  self.conn.cursor()


        except Exception,e:
            logging.error('connect database error!'+str(e))
            return
        
        #应用列表
        self.HOST=[]
        
        #探测结果变量
        self.FID = 0
        self.NAMELOOKUP_TIME =  0.0
        self.CONNECT_TIME =  0.0
        self.PRETRANSFER_TIME =  0.0
        self.STARTTRANSFER_TIME =  0.0
        self.TOTAL_TIME = 0.0
        self.HTTP_CODE =  '000'
        self.SIZE_DOWNLOAD =  0
        self.HEADER_SIZE = 0
        self.REQUEST_SIZE = 0
        self.CONTENT_LENGTH_DOWNLOAD=0
        self.SPEED_DOWNLOAD=0.0
        self.DATETIME=0
        self.MARK=0
        
        #探测结果元组
        self.RunResult=()

    #虚构方法
    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception,e:
            logging.debug('__del__ object error!'+str(e))

    #报警方法
    def Alarm(self,notificationtype,target,content):
        try:
            import urllib
            #InterfaceURL="http://Alarms.domain.com/sendmail/"+notificationtype+"/"+target+"/"+content
            #print "InterfaceURL is: ",InterfaceURL
            #_GetResult=urllib.urlopen(InterfaceURL)

            if notificationtype=="email":
                import smtplib
                from email.mime.text import MIMEText
                from email.header import Header

                sender = 'kylin@wanxue.cn'
                receiver = target



                subject = '告警通知：'+content
                smtpserver = 'mail.wanxue.cn'
                username = 'kylin'
                password = 'wx1212psd'


                #中文需参数‘utf-8'，单字节字符不需要
                msg = MIMEText(content,'text','utf-8')
                msg['Subject'] = Header(subject, 'utf-8')

                smtp = smtplib.SMTP()
                smtp.connect('mail.wanxue.cn')
                smtp.login(username, password)
                smtp.sendmail(sender, receiver, msg.as_string())
                smtp.quit()
            elif notificationtype=="weixin":
                ##微信报警
                print 'notificationtype IS ====>:',notificationtype
                print "aleart content is :",content
                if content:
                    with open(r'./wx_msg.txt','ab') as f:
                        ####定义时间转换格式
                        tran_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                        print tran_time
                        f.write(content+'\r\n')
                ##获取生成token
                weixin.generate_token()
                print"+++1"
                ##群发消息
                weixin.test_txt()
                print"+++2"
                ##发完后消息，清空消息。
                with open(r'./wx_msg.txt','w') as f:
                        f.write('\r\n')


        except Exception,e:
            logging.debug('Alarm error!'+str(e))

    #探测主机响应信息
    #状态说明
    #200 正常
    #000 返回串不相等
    #str(e)异常信息

    def runhost(self):
        for _hostlist in self.HOST:
            print "=======_hostlist is =======>>>>>>>",_hostlist
            self.FID = int(_hostlist[0])

            self.DATETIME=int(str(time.time()).split('.')[0])
            if _hostlist[3]=="weixin":
                _target=MOBILETO
                _contentheader=""
            else:
                _target=MAILTO
                _contentheader="应用异常报警通知^@"
            try:
                url = _hostlist[1].strip()
                Curlobj = pycurl.Curl()
                Curlobj.setopt(Curlobj.URL, url)
                
                #连接的等待时间
                Curlobj.setopt(Curlobj.CONNECTTIMEOUT, CONNECTTIMEOUT)
                
                #请求超时时间
                Curlobj.setopt(Curlobj.TIMEOUT, TIMEOUT)
                Curlobj.setopt(Curlobj.NOPROGRESS, 0)
                Curlobj.setopt(Curlobj.FOLLOWLOCATION, 1)#设置写的回调，所有输出都定向到bodyfile中
                Curlobj.setopt(Curlobj.MAXREDIRS, 5)#重定向次数
                Curlobj.setopt(Curlobj.OPT_FILETIME, 1)
                Curlobj.setopt(Curlobj.NOPROGRESS, 1)
                Curlobj.setopt(pycurl.USERAGENT,"Mozilla/5.0")#设置代理浏览器
                bodyfile = open(os.path.dirname(os.path.realpath(__file__))+"/_body", "wb")
                Curlobj.setopt(Curlobj.WRITEDATA, bodyfile)#输出文件保存到_body里面
                Curlobj.perform()
                bodyfile.close()

                self.NAMELOOKUP_TIME =  Decimal(str(round(Curlobj.getinfo(Curlobj.NAMELOOKUP_TIME), 2)))
                self.CONNECT_TIME =  Decimal(str(round(Curlobj.getinfo(Curlobj.CONNECT_TIME),2)))
                self.PRETRANSFER_TIME =   Decimal(str(round(Curlobj.getinfo(Curlobj.PRETRANSFER_TIME),2)))
                self.STARTTRANSFER_TIME = Decimal(str(round(Curlobj.getinfo(Curlobj.STARTTRANSFER_TIME),2)))
                self.TOTAL_TIME = Decimal(str(round(Curlobj.getinfo(Curlobj.TOTAL_TIME),2)))
                self.HTTP_CODE =  Curlobj.getinfo(Curlobj.HTTP_CODE)
                self.SIZE_DOWNLOAD =  Curlobj.getinfo(Curlobj.SIZE_DOWNLOAD)
                self.HEADER_SIZE = Curlobj.getinfo(Curlobj.HEADER_SIZE)
                self.REQUEST_SIZE = Curlobj.getinfo(Curlobj.REQUEST_SIZE)
                self.CONTENT_LENGTH_DOWNLOAD=Decimal(str(round(Curlobj.getinfo(Curlobj.CONTENT_LENGTH_DOWNLOAD),2)))
                self.SPEED_DOWNLOAD=Curlobj.getinfo(Curlobj.SPEED_DOWNLOAD)

                if str(_hostlist[4])!="200":
                    returncontent=''.join(open(os.path.dirname(os.path.realpath(__file__))+'/_body', 'rb').readline().split())

                    if _hostlist[4]!=returncontent:
                        #返回串不一致
                        self.HTTP_CODE="000"
                        #报警
                        ####生成content报警内容
                        self.Alarm(_hostlist[3],_target,_contentheader+"探测["+_hostlist[5]+"]应用返回串与设定值不一致")

                elif str(_hostlist[4])=="200" and str(self.HTTP_CODE)!="200":
                    #返回 http status为非200
                    #报警
                    ####生成content报警内容
                    self.Alarm(_hostlist[3],_target,_contentheader+"探测["+_hostlist[5]+"]应用返回非200状态("+str(self.HTTP_CODE)+")")



            except Exception,e:
                self.NAMELOOKUP_TIME =  0.0
                self.CONNECT_TIME =  0.0
                self.PRETRANSFER_TIME =  0.0
                self.STARTTRANSFER_TIME =  0.0
                self.TOTAL_TIME = 0.0
                self.HTTP_CODE =  str(e).replace("'","\''")
                self.SIZE_DOWNLOAD =  0
                self.HEADER_SIZE = 0
                self.REQUEST_SIZE = 0
                self.CONTENT_LENGTH_DOWNLOAD=0
                self.SPEED_DOWNLOAD=0.0
                self.MARK=0
                logging.error('pycurl url reset:'+str(e))
                #报警
                ####生成content报警内容
                self.Alarm(_hostlist[3],_target,_contentheader+"探测["+_hostlist[5]+"]应用超时或连接异常")

                pass

            self.RunResult=(self.FID,self.NAMELOOKUP_TIME,self.CONNECT_TIME,self.PRETRANSFER_TIME,self.STARTTRANSFER_TIME,self.TOTAL_TIME, \
                        self.HTTP_CODE,self.SIZE_DOWNLOAD,self.HEADER_SIZE,self.REQUEST_SIZE,self.CONTENT_LENGTH_DOWNLOAD,self.SPEED_DOWNLOAD, \
                        self.DATETIME,self.MARK)
            try:
                self.cursor.execute("insert into webmonitor_monitordata (`id`, `FID`, `NAMELOOKUP_TIME`, `CONNECT_TIME`, `PRETRANSFER_TIME`, `STARTTRANSFER_TIME`, `TOTAL_TIME`, `HTTP_CODE`, `SIZE_DOWNLOAD`, `HEADER_SIZE`, `REQUEST_SIZE`, `CONTENT_LENGTH_DOWNLOAD`, `SPEED_DOWNLOAD`, `DATETIME`, `MARK`) VALUES (0,'%d','%f','%f','%f','%f','%f','%s','%f','%d','%d','%f','%f','%d','%d')"%(self.RunResult))
                self.conn.commit()
            except Exception,e:
                logging.debug('monitordata insert error:'+str(e))

            Curlobj.close()


    #获取主机信息
    def readhost(self):
        self.cursor.execute('select id,url,isp,alarmtype,alarmconditions,appname from webmonitor_monitorappinfo where isp="%s"' %(isp,))
        for row in self.cursor.fetchall():
            self.HOST.append(row)



    #获取URL域名
    def GetURLdomain(self,url):
        xurl=""
        if url[:7]=="http://":
            xurl=url[7:]
        else:
            xurl=url
        return string.split(xurl,'/')[0]


if __name__ == '__main__':
    app=Runmonitor()
    app.readhost()
    app.runhost()
    print app.HOST

