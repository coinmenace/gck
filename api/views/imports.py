# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import *
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader
from django.db.models import *
from api.models import *
import time
import csv
from django.utils import timezone
from django.utils.encoding import *
import hashlib
from celery.result import AsyncResult
from celery.task.control import *
from celery import task, current_task,current_app
import os
import codecs
import json
from celery import Celery
from django.conf import settings
from anyjson import serialize
import uuid
from os import listdir
from os.path import isfile, join
from django import template
from PIL import Image
from  django.core.files.images import ImageFile
import messages as MESSAGE
from smsgateway import SMSGateway
from random import *
import settings
import redis
rdb = redis.Redis()
# Create your views here.
siteurl=settings.siteurl
data={}


def verifySignature(req):
    request=req
    sig_verify={}
    if "HTTP_X_AP_SIGNATURE" not in request.META:
        sig_verify['status']="invalid signature"
    elif "HTTP_X_NL_API_VERSION" not in request.META:
        sig_verify['status']="unknown api version"
    elif "HTTP_VERSION" not in request.META:
        sig_verify['status']="unknown app version"
    elif "HTTP_X_NL_KEY" not in request.META:
        sig_verify['status']="invalid key"
    else:
        sig_verify['status']="ok"
    if sig_verify['status']!="ok":
        data={}
        data['status']="failed"
        data['message']=sig_verify['status']
    else:
        data={}
        data['status']="ok"
    data['status']="ok"
    return data

def get2FACode():
    n=6
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def sendMessage(recipient,message):
    url = "https://api.infobip.com/"
    username = "lp_app"
    password = "Legalp1234"
    s=SMSGateway(url,username,password)
    method="GET"
    endpoint = "sms/1/text/single"
    params={}
    params['username']=username
    params['password']=password
    params['from']=settings.SITENAME
    params['to']=recipient
    params['text']= message
    s.sendMessage(method,endpoint,params)

def generateTempPassword():
    n=6
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def checkActiveUser(uid,deviceid,sessionid):
    print uid,deviceid,sessionid
    userkey="user_"+str(uid)
    savedkey = rdb.get(userkey)
    data={}
    if savedkey !=None:
        print "user exist"
        print str(savedkey)
        try:
            jsondata = str(savedkey).replace('u\'','\'').replace('\'','"')
            print jsondata
            userdata = json.loads(jsondata)
        except Exception as ex:
            print ex
        print userdata
        print "Done 1"
        print userdata['device']
        if userdata['device']!=deviceid:
            print "You have logged in from another device"
            data['requires_verification']=True
        else:
            data['requires_verification'] = False
        print "Done 2"
        print userdata['sessionid']
        if userdata['sessionid']!=sessionid:
            userdata['sessionid'] = sessionid
            rdb.set(userkey, userdata)
            data['session_changed'] = True
        else:
            data['session_changed'] = False
        print "Done 3"

    else:
        userdata ={'uid':uid,'device':deviceid,'sessionid':sessionid}
        userdata=json.dumps(userdata)
        print userdata
        rdb.set(userkey,userdata)
        data['session_changed'] = False
        data['requires_verification'] = False
    return data


def convertToInternationalNumber(receipient):
    if receipient[0]=="0":
        number = "234"+receipient[1:]
    else:
        number= receipient
    print number
    return number