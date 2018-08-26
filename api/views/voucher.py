from imports import *

#this needs to be protected in a way
@csrf_exempt
def voucherwallet(request):
    amount = request.POST.get("amount")
    uid = request.POST.get("uid")
    user = User.objects.get(id=uid)
    data={}
    if user!=None:
        wallet = Wallet.objects.get(uid=uid)
        balance = wallet.balance
        if balance>int(amount):
            amounttrans = int(amount)
            newbalance = balance - int(amount)
            wallet.balance = newbalance
            wallet.save()
            pid=-1
            genuuid = uuid.uuid4()
            vouchercode = str(generateVoucherCode())
            description="Voucher generation from wallet by "+user.username+" for amount "+str(amount)
            transactionid = str(genuuid.hex.upper())
            transaction = Transactions.objects.create(pid=pid, uid=uid, tax=0.0, commission=0.0, voucher_code="",
                                                      amount=amounttrans, reference=transactionid, otherref="N/A",
                                                      description=description, status=0,
                                                      createdate=timezone.now())
            tid = transaction.id
            voucherid = Voucher.objects.create(uid=uid, tid=tid, vouchercode=vouchercode, amount=amounttrans,status=0, createdate=timezone.now())
            data['status'] = "ok"
            data['message'] = "successfully generated voucher.Your Voucher Code is :"+vouchercode
            return JsonResponse(data)
        else:
            data['status']="failed"
            data['message']="you do not have enough funds to generate this voucher"
            return JsonResponse(data)
    else:
        data['status'] = "failed"
        data['message'] = "invalid user"
        return JsonResponse(data)




@csrf_exempt
def vouchergift(request):
    template = loader.get_template('voucher_payment_home.html')
    amount = request.POST.get("amount")
    pid=-1
    if "uid" in request.session:
        uid=request.session.get("uid")
    else:
        uid = request.POST.get("uid")
        request.session['uid']=uid
    profile=Profile.objects.get(uid=uid)
    data['payment_gateway']="paystack"#"kongapay"
    data['merchantid']=settings.payment_merchant_id  #"testmerchant"
    data['merchantname']="Ridit"
    data['phone']=profile.telephone
    data['callbackurl']=siteurl+"/api/v1/voucher/pay"
    data['amount']=str(amount)
    data['email']=profile.email
    genuuid=uuid.uuid4()
    data['transid']=genuuid.hex.upper()
    data['description']="Gift A Audio Book of "+amount
    try:
        transaction=Transactions.objects.create(pid=pid,uid=uid,tax=0.0,commission=0.0,voucher_code="",amount=data['amount'],reference=data['transid'],otherref="",description=data['description'],status=0,createdate=timezone.now())
        data['transactionid']=transaction.id
    except Exception as ex:
        print ex
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))


def voucherpay(request):
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
    uid=request.session.get("uid")
    data={}
    if transaction.status==1:
        data['message']="Successfully generated voucher"
        data['pid'] = pid
        voucher = Voucher.objects.get(tid=transactionid)
        vouchercode = voucher.vouchercode
        data['vouchercode'] = vouchercode
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
            vouchercode = str(generateVoucherCode())
            voucerid = Voucher.objects.create(uid=uid,tid=transactionid,vouchercode=vouchercode,amount=amounttrans,status=0,createdate=timezone.now())
            data['vouchercode'] = vouchercode
            data['message']="Successfully generated voucher"
            data['pid'] = pid
        else:
            data['message']="Amount does not match"
    else:
        data['message']="Unable to complete payment ("+reason+")"

    template = loader.get_template('voucher_payment_completed.html')
    context = {
        'data': data
        }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def voucherredeem(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            code = request.POST.get("vouchercode")
            uid = request.POST.get("uid")
            data={}
            try:
                voucher =  Voucher.objects.filter(Q(vouchercode=code))
                print len(voucher)
                if len(voucher)>0:
                    if voucher[0].usedbyid == int(uid):
                        data['status'] = "ok"
                        data['message'] = "voucher has already been used by you"
                        return JsonResponse(data)
                    if voucher[0].status == 1:
                        data['status']="ok"
                        data['message']="voucher has already been used"
                        return JsonResponse(data)
                    amount = voucher[0].amount
                    wallet = Wallet.objects.get(uid=uid)
                    walletbalance = wallet.balance
                    wallet.balance = walletbalance + amount
                    wallet.save()
                    voucher[0].usedbyid = uid
                    voucher[0].status = 1
                    voucher[0].save()
                    data['status'] = "ok"
                    data['message'] = "voucher has been credited to your wallet"
                    return JsonResponse(data)
                else:
                    data['status'] = "failed"
                    data['message'] = "no such voucher exist"
            except Exception as ex:
                print ex
                data['status']="failed"
                data['message']="unable to redeem voucher"
                return JsonResponse(data)
        else:
            data={}
            data['status']="failed"
            data['message']=MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']=MESSAGE.INVALID_SESSION
    return JsonResponse(data)

def generateVoucherCode():
    n=8
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)