# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader
from django.db.models import *
from api.models import *
import uuid
from django.utils import timezone
from django.utils.encoding import *
import settings
import requests
from smsgateway import *
from random import *
import json
from django.views.decorators.clickjacking import xframe_options_exempt
# Create your views here.
siteurl=settings.siteurl
# Create your views here.
data={}

@xframe_options_exempt
def index(request):
    template = loader.get_template('payment_home.html')
    print "Welcome home"
    data['sitename']="Ridit"
    context = {
        'data': data
    }
    return HttpResponse(template.render(context, request))

@xframe_options_exempt
def dopay(request):
    template = loader.get_template('payment_process.html')
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    amount = request.POST.get("amount")
    pid = -1
    data['payment_gateway'] = "paystack"  # "kongapay"
    data['merchantid'] = settings.payment_merchant_id  # "testmerchant"
    data['merchantname'] = "Flamemediaworks"
    data['phone'] = phone
    request.session['phone'] = phone
    data['callbackurl'] = siteurl+"/payment/completed"
    data['amount'] = str(int(amount))
    data['email'] = phone
    uid = -1
    genuuid = uuid.uuid4()
    data['email'] = email
    data['transid'] = genuuid.hex.upper()
    data['description'] = "Gift of Audio Book for  " + amount+" by "+phone
    try:
        transaction = Transactions.objects.create(pid=pid, uid=uid, tax=0.0, commission=0.0, voucher_code="",
                                                  amount=data['amount'], reference=data['transid'], otherref="",
                                                  description=data['description'], status=0, createdate=timezone.now())
        data['transactionid'] = transaction.id
    except Exception as ex:
        print ex
    context = {
        'data': data
    }
    return HttpResponse(template.render(context, request))


@xframe_options_exempt
def paymentcompleted(request):
    url = "https://api.paystack.co/transaction/verify/"
    txnref = request.GET.get('reference', 'Not Available')
    transactionid = request.GET.get('transactionid', 0)
    fullurl = url + txnref
    secret_key = settings.payment_secret_key
    headers = {"Authorization": "Bearer " + secret_key}
    res = requests.get(fullurl, headers=headers)
    response = json.loads(res.content)
    gatewaystatus = response['data']['status']
    amountgateway = response['data']['amount']
    reason = response['data']['gateway_response']
    transaction = Transactions.objects.get(id=transactionid)
    pid = transaction.pid
    amounttrans = transaction.amount * 100
    uid = request.session.get("uid")
    data = {}
    if transaction.status == 1:
        data['message'] = "Successfully generated voucher"
        data['pid'] = pid
        voucher = Voucher.objects.get(tid=transactionid)
        vouchercode = voucher.vouchercode
        data['vouchercode'] = vouchercode
    elif gatewaystatus and transaction.status == 0:

        if amountgateway == amounttrans:
            transaction.status = 1
            transaction.otherref = txnref
            transaction.save()
            status = 1
            comment = gatewaystatus
            purchase = Purchases.objects.create(uid=uid, pid=pid, comment=comment,
                                                amount=amounttrans, tax=0.0, commission=0.0, status=status,
                                                createdate=timezone.now())
            vouchercode = str(generateVoucherCode())
            voucerid = Voucher.objects.create(uid=uid, tid=transactionid, vouchercode=vouchercode, amount=amounttrans,
                                              status=0, createdate=timezone.now())
            data['vouchercode'] = vouchercode
            data['message'] = "Successfully generated voucher"
            data['pid'] = pid
            recipient = request.session.get("phone")
            try:
                sendMessage(recipient, vouchercode)
            except Exception as ex:
                print ex
        else:
            data['message'] = "Amount does not match"
    else:
        data['message'] = "Unable to complete payment (" + reason + ")"

    template = loader.get_template('voucher_payment_completed.html')
    context = {
        'data': data
    }
    return HttpResponse(template.render(context, request))


def generateVoucherCode():
    n=8
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def sendMessage(recipient,code):
    url="http://www.estoresms.com"
    username="biddyweb"
    password="googleboy234"
    s=SMSGateway(url,username,password)
    method="GET"
    endpoint="smsapi.php"
    params={}
    params['username']=username
    params['password']=password
    params['sender']=settings.SITENAME
    params['recipient']=recipient
    params['message']="You have successfully generated a gift voucher on "+settings.SITENAME+".The voucher code is: "+str(code)
    s.sendMessage(method,endpoint,params)