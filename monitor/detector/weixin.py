# -*- coding: utf-8 -*-
import urllib2
from urllib import urlencode
import json,time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')#wx only adapt utf-8 (no unicode,no encoding and stay what it looks like)
from config import *
Debug = True
IsFlag = True

def getTokenIntime(CorpId,Secret):
    res = urllib2.urlopen('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s'%(CorpId,Secret))
    res_dict = json.loads(res.read())
    token = res_dict.get('access_token',False)
    print token,"=====>>>token"
    if not token:
        with open(r'./wx_log.txt','ab') as f:
            f.write(u'异常: 无法取得token')
    return token

def getToken():
    with open(r'./wx_token.txt') as f:
        t = f.read()
    return t
    


def sendTxtMsg(token,content,to_user='@all',to_party='',to_tag='',application_id=0,safe=0):
    try:
        data = {
           "touser": to_user,
           "toparty": to_party,
           "totag": to_tag,
           "msgtype": "text",
           "agentid": application_id,
           "text": {
               "content": content,
           },
           "safe":safe
        }

        data = json.dumps(data,ensure_ascii=False)
        if Debug:
            with open(r'./wx_data.txt','ab') as f:
                f.write(data+'\r\n')

        req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s'%(token,))        
        resp = urllib2.urlopen(req,data)
        msg = u'返回值:' + resp.read()
    except Exception,ex:
        msg = u'异常:' + str(ex)
    finally:
        with open(r'./wx_log.txt','ab') as f:

            f.write(msg+'\r\n')



def sendNews(token,title,description,url,pic_url,to_user="@all",to_party="",to_tag="",application_id=0,safe=0):
    try:
        data = {
           "touser": to_user,
           "toparty": to_party,
           "totag": to_tag,
           "msgtype": "news",
           "agentid": application_id,
           "news": {
               "articles":[
                   {
                       "title": title,
                       "description": description,
                       "url": url,
                       "picurl": pic_url,
                   }    
               ]
           }
        }
     
        data = json.dumps(data,ensure_ascii=False)
        if Debug:
            with open(r'./wx_data.txt','ab') as f:
                f.write(data+'\r\n')

        req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/message/send?debug=1&access_token=%s'%(token,))
        resp = urllib2.urlopen(req,data)
        msg = u'返回值:' + resp.read()
    except Exception,ex:
        msg = u'异常:' + str(ex)
    finally:
        with open(r'./wx_log.txt','ab') as f:
            f.write(msg+'\r\n')
def send_btn(token,application_id=0):
    try:
        req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/menu/create?access_token=%s&agentid=%s'%(token,application_id))
        data = {
           "button":[
               {	
                   "type":"view",
                   "name":"search",
                   "url":"http://www.baidu.com/",
               },

           ]
        }
        data = json.dumps(data,ensure_ascii=False)
        res = urllib2.urlopen(req,data)
        msg = u'返回值:'+res.read()
    except Exception,ex:
        msg = u'异常:'+str(ex)
    finally:
        with open(r'./wx_log.txt','ab') as f:
            f.write(msg+'\r\n')

    

def generate_token():
    with open(r'./wx_token.txt','wb') as f:
        if IsFlag:
            f.write(getTokenIntime('wx811b*****','DIG0IYF5iyJEe0K6jIM***'))
        else:            
            f.write(getTokenIntime('wx811b*****','0000O'))
            
            
def get_msg():
    with open(r'wx_msg.txt','rb') as f:
        txt = f.read()
    txt = txt.replace('\r\n','').replace('\r','').replace('\n','').replace('\t','')
    return txt

#======================================test ==========================

def test_txt():
    txt = get_msg()
    token = getToken()
    if token:
        sendTxtMsg(token, txt)

def test_news():
    img_url = 'http://d.hiphotos.baidu.com/image/w%3D2048/sign=a29e35bb8813632715edc533a5b7a1ec/d8f9d72a6059252d676bb463369b033b5bb5b95d.jpg'
    token = getToken()
    if token:
        sendNews(token, u'测试新闻', get_msg(), 'http://news.baidu.com', img_url)

def test_sb():
    token = getToken()
    if token:
        send_btn(token,application_id=1)

if __name__ == '__main__':

    generate_token()

    test_txt()
#test_news()
#test_sb()

