# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader
from django.db.models import *
from .models import *
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
from celery import Celery
from django.conf import settings
from anyjson import serialize
import uuid
from os import listdir
from os.path import isfile, join
from django import template
import uuid
import requests

# Create your views here.
data={"sitename":"Ridit"}
def index(request):
    template = loader.get_template('index.html')
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))

#post
#phone,amount,email,description
@csrf_exempt
def payment(request):
    template = loader.get_template('payment.html')
    data['payment_gateway']="paystack"#"kongapay"
    data['merchantid']="pk_test_294b393b858f07d85789bc1d0029a482568cf605" #"testmerchant"
    data['merchantname']="audioApp"
    data['phone']=request.POST.get('phone','Not Available')
    data['callbackurl']="http://fma.mobilipia.com/completed"
    data['amount']=request.POST.get('amount','0')
    data['email']=request.POST.get('email','Not Available')
    uid=uuid.uuid4()
    data['transid']=uid.hex.upper()
    data['description']=request.POST.get('description','Not Available')
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def paymentcompleted(request):
    print request.POST.get
    url="https://api.paystack.co/transaction/verify/"
    txnref=request.POST.get('txnref','Not Available')
    fullurl=url+txnref
    secret_key="sk_test_b9ffbfbaf3f29559d8945aed1b11b8b7d1db708a"
    headers={"Authorization":" Bearer "+secret_key}
    res=requests.get(fullurl,headers=headers)
    data={}
    data['data']=res.content
    return JsonResponse(data)