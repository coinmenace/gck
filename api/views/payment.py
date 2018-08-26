from imports import *




@csrf_exempt
def payment(request):
    template = loader.get_template('api_payment_home.html')
    pid=request.POST.get("pid")
    pinfo=Product.objects.get(id=pid)
    if "uid" in request.session:
        uid=request.session.get("uid")
    else:
        uid = request.POST.get("uid")
        request.session['uid']=uid
    profile=Profile.objects.get(uid=uid)
    data['payment_gateway']="paystack"#"kongapay"
    data['merchantid'] = settings.payment_merchant_id#"testmerchant"
    data['merchantname']="Flamemediaworks"
    data['phone']=profile.telephone
    data['callbackurl']=siteurl+"/api/v1/payment/completed"
    data['amount']=str(int(pinfo.price))
    data['email']=profile.email
    genuuid=uuid.uuid4()
    data['transid']=genuuid.hex.upper()
    data['description']="Payment for "+pinfo.name
    try:
        transaction=Transactions.objects.create(pid=pid,uid=uid,tax=0.0,commission=0.0,voucher_code="",amount=data['amount'],reference=data['transid'],otherref="",description=data['description'],status=0,createdate=timezone.now())
        data['transactionid']=transaction.id
    except Exception as ex:
        print ex
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))


def paymentcompleted(request):
    url="https://api.paystack.co/transaction/verify/"
    txnref=request.GET.get('reference','Not Available')
    transactionid=request.GET.get('transactionid',0)
    fullurl=url+txnref
    secret_key = settings.payment_secret_key
    headers={"Authorization":"Bearer "+secret_key}
    res=requests.get(fullurl,headers=headers)
    response=json.loads(res.content)
    gatewaystatus=response['data']['status']
    amountgateway=response['data']['amount']
    reason=response['data']['gateway_response']
    transaction=Transactions.objects.get(id=transactionid)
    pid=transaction.pid
    amounttrans=transaction.amount*100
    pinfo=Product.objects.get(id=pid)
    uid=request.session.get("uid")
    data={}
    if transaction.status==1:
        data['message']="Successfully purchased product"
        data['pid'] = pid
    elif gatewaystatus and transaction.status==0:

        if amountgateway==amounttrans:
            transaction.status=1
            transaction.otherref=txnref
            transaction.save()
            status=1
            comment=gatewaystatus
            purchase = Purchases.objects.create(uid=uid, pid=pid, comment=comment,
                                                amount=amounttrans, tax=0.0, commission=0.0, status=status,
                                                createdate=timezone.now())

            data['message']="Successfully purchased product"
            data['pid'] = pid
        else:
            data['message']="Amount does not match"
    else:
        data['message']="Unable to complete payment ("+reason+")"

    template = loader.get_template('api_payment_completed.html')
    context = {
        'data': data
        }
    return HttpResponse(template.render(context, request))


def requestpurchasetransaction(request):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            uid = request.session.get("uid")
            productid = request.GET.get("pid")
            print "Product ID ", productid
            product = Product.objects.filter(id=productid).all()
            contentid = product[0].contentid
            content = Content.objects.filter(identifier=contentid).all()
            c = content[0]
            p = product[0]
            purchase = Purchases.objects.get(uid=uid,pid=productid)
            purchasedata = getPurchaseDict(p, purchase, c)
            print purchasedata
            mediaid = p.id
            title = p.name
            handleContentrating(mediaid, title)
            data = {}
            data['products'] = purchasedata
            data['status'] = "ok"
            return JsonResponse(data)
        else:
            data = {}
            data['status'] = "failed"
            data['message'] = MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data = {}
        data['status'] = "failed"
        data['message'] = MESSAGE.INVALID_SESSION
        return JsonResponse(data)
