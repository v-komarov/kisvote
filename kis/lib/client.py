#!/usr/bin/python
#coding:utf-8

#import pyrad.packet
#from pyrad.client import Client
#from pyrad.dictionary import Dictionary
import urllib2
import json
from kis.settings import AUTHSERVICE




def AuthUser(login,password,request):

    url = "http://{}?action=user-kis&login={}&passwd={}".format(AUTHSERVICE,login,password)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    d = json.loads(response.read())
    if d['result'] == u'ok':
        request.session['key999'] = d
        return "access accepted"
    else:
        return "access denied"
