#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'cwm'
from django import forms
from webmonitor.models import MonitorAppInfo,MonitorData
from django.core.exceptions import ValidationError
import re

def url_valid_data(value):
    """
    #完整域名合法性检测，例如:www.baidu.com正则表达式：^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$
    #匹配网址，例如： http://www.baidu.com 正则表达式：^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*$
    #匹配http url,例如:http://www.tetet.com/index.html?q=1&m=test 正则表达式：^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*([\?&]\w+=\w*)*$
    #严格匹配，http://开头，匹配URL,IP，带参数，端口号  正则表达式：((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?
    :param value:
    :return:
    """

    url_re4=re.compile(r'((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?')
    #url_re2 = re.compile(r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*$')
    #url_re3 = re.compile(r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*([\?&]\w+=\w*)*$')

    url_re1=re.compile(r'^(http://)?[a-zA-Z0-9]+(.[a-zA-Z0-9]+)*(\w|/)+$')
    if not url_re1.match(value):
        raise ValidationError('URL格式错误')



def alarmconditions_valid_data(value):
    alarmconditions_re=re.compile(r'^[0-9]*$')
    if not alarmconditions_re.match(value):
        raise ValidationError('状态码输入不合法')


class MonitorinfoForm(forms.ModelForm):
    ISP_CHOICES = (
        (u'ct', '中国电信'),
        (u'cnc', '中国联通'),
        (u'cmcc', '中国移动'),
                    )

    attrs_dict = {'class': 'form-control'}
    isp = forms.CharField(widget=forms.Select(choices=ISP_CHOICES,attrs=attrs_dict))
    url = forms.CharField(validators=[url_valid_data,],widget=forms.TextInput(attrs=attrs_dict))
    alarmconditions = forms.CharField(validators=[alarmconditions_valid_data,],widget=forms.TextInput(attrs=attrs_dict))
    class Meta:

        model = MonitorAppInfo
        fields = ('appname','url','isp','alarmtype','alarmconditions')

        widgets = {
            'appname' : forms.TextInput(attrs={'class':'form-control'}),

             'alarmtype' : forms.RadioSelect(choices=((u'weixin', u'微信报警'),(u'email', u'邮件通知'),),attrs={'class':'list-inline'}),

        }


    def __init__(self, *args, **kwargs):
        super(MonitorinfoForm, self).__init__(*args, **kwargs)
        self.fields['appname'].label = u'业务名称'
        self.fields['appname'].error_messages={'required':u'请输入监控应用（业务线）'}
        self.fields['url'].label = u'监控URL'
        self.fields['url'].error_messages={'required':u'请输入URL地址'}
        self.fields['isp'].label = u'侦测线路'
        self.fields['isp'].error_messages={'required':u'请选择运营商线路'}
        self.fields['alarmtype'].label = u'通知方式'
        self.fields['alarmtype'].error_messages={'required':u'请选择告警通知方式'}
        self.fields['alarmconditions'].label = u'状态码'
        self.fields['alarmconditions'].error_messages={'required':u'请输入探测码'}





class EditMonitorinfoForm(forms.ModelForm):
    ISP_CHOICES = (
        (u'ct', '中国电信'),
        (u'cnc', '中国联通'),
        (u'cmcc', '中国移动'),
                    )

    attrs_dict = {'class': 'form-control'}
    isp = forms.CharField(widget=forms.Select(choices=ISP_CHOICES,attrs=attrs_dict))
    url = forms.CharField(validators=[url_valid_data,],widget=forms.TextInput(attrs=attrs_dict))
    alarmconditions = forms.CharField(validators=[alarmconditions_valid_data,],widget=forms.TextInput(attrs=attrs_dict))
    class Meta:
        model = MonitorAppInfo
        fields = ('appname','url','isp','alarmtype','alarmconditions')
        widgets = {
            'id':forms.IntegerField(),
            'appName' : forms.TextInput(attrs={'class':'form-control'}),
             'alarmtype' : forms.RadioSelect(choices=((u'weixin', u'微信报警'),(u'email', u'邮件通知'),),attrs={'class':'list-inline'}),


        }


    def __init__(self, *args, **kwargs):
        super(EditMonitorinfoForm, self).__init__(*args, **kwargs)
        self.fields['appname'].label = u'业务名称'
        self.fields['appname'].error_messages={'required':u'请输入监控应用（业务线）'}
        self.fields['url'].label = u'监控URL'
        self.fields['url'].error_messages={'required':u'请输入URL地址'}
        self.fields['isp'].label = u'侦测线路'
        self.fields['isp'].error_messages={'required':u'请选择运营商线路'}
        self.fields['alarmtype'].label = u'通知方式'
        self.fields['alarmtype'].error_messages={'required':u'请选择告警通知方式'}
        self.fields['alarmconditions'].label = u'状态码'
        self.fields['alarmconditions'].error_messages={'required':u'请输入探测码'}


class HomeForm(forms.Form):


    admin = forms.IntegerField(
        widget=forms.Select(choices="1234")
    )
    def __init__(self, *args, **kwargs):
        super(HomeForm, self).__init__(*args, **kwargs)

        self.fields['admin'].widget.choices = MonitorAppInfo.objects.all().values_list('id', 'appname')
