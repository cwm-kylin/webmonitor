# -*- coding: utf-8 -*-

from django import template
from webmonitor.public import *
from webmonitor.models import MonitorAppInfo


register = template.Library()

def result_domain(value):
    return GetURLdomain(value)

def result_datetime(value):
    return stamp2time(value)


register.filter(result_domain)
register.filter(result_datetime)

