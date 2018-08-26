from imports import *

#purchase
#@csrf_protect
@csrf_exempt
def purchase(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            data={}
            try:
                uid=request.POST.get("uid")
                productid=request.POST.get("productid")
                paymenttype=int(request.POST.get("paymenttype"))
                if int(request.session.get("uid"))!=int(uid):
                    data={}
                    data['status']="failed"
                    data['message']=MESSAGE.INVALID_USERID
                    return JsonResponse(data)
                purchases=Purchases.objects.filter(Q(uid=uid) & Q(pid = productid)).all()

                if len(purchases)>0:
                    data={}
                    data['status']="ok"
                    data['message']=MESSAGE.ITEM_PURCHASED
                    p=Product.objects.filter(id=productid).all()
                    contentid=p[0].contentid
                    content=Content.objects.filter(identifier=contentid).all()
                    c=content[0]
                    p=p[0]
                    purchase=purchases[0]
                    author = Author.objects.get(id=p.authorid)
                    purchasedata = getPurchaseDict(p,purchase,c,author)
                    data['products']=purchasedata
                    try:
                        title=p.name
                        contentid=str(p.id)
                        likes=0
                        listen=0
                        download=0
                        c=ContentRating.objects(contentid=contentid,uid=uid)
                        print "fetching from mongo ",c
                        if c.count()<=0:
                            download=download+1
                            c=ContentRating(contentid =contentid ,uid=uid,like=likes,listen=listen,download=download,title =title ,createdate = timezone.now())
                            c.save()
                        else:
                            download=int(c[0].download)+1
                            c[0].update(download=download)

                    except Exception as ex:
                        print ex
                    return JsonResponse(data)
                uid=request.session.get("uid")
                product=Product.objects.filter(Q(id=productid)).all()
                purchaseamount=int(product[0].price)
                if paymenttype==1:
                    print "Got here"
                    wallet=Wallet.objects.filter(Q(uid=uid)).all()
                    currentbalance=int(wallet[0].balance)
                    print "user balance ",currentbalance
                    print "amount ",purchaseamount
                    if currentbalance<purchaseamount:
                        data={}
                        data['status']="failed"
                        data['message']=MESSAGE.INSUFFICIENT_FUNDS
                        return JsonResponse(data)
                    newbalance=currentbalance-purchaseamount
                    wallet.update(balance=newbalance)
                    comment=""
                    status=1
                    purchase=Purchases.objects.create(uid=uid,pid = productid,comment = comment,
                    amount =purchaseamount ,tax = 0.0,commission = 0.0, status = status,
                    createdate =timezone.now())
                    #this should return the info about the purchase
                    #the license key
                    #the secret key
                    print "Product ID ",productid
                    product=Product.objects.filter(id=productid).all()
                    contentid=product[0].contentid
                    content=Content.objects.filter(identifier=contentid).all()
                    c=content[0]
                    p=product[0]
                    author = Author.objects.get(id=p.authorid)
                    purchasedata=getPurchaseDict(p,purchase,c,author)
                    print purchasedata
                    data={}
                    data['products']=purchasedata
                    data['status']="ok"
                    data['message']=MESSAGE.PURCHASE_SUCCESS
                else:
                    data={}
                    data['status']="ok"
                    data['message']=MESSAGE.PAYMENT_UNSUPPORTED
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']=MESSAGE.PURCHASE_FAIL
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






#purchase
#@csrf_protect
@csrf_exempt
def rate(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            data={}
            try:
                uid=request.POST.get("uid")
                productid=request.POST.get("rating")
                paymenttype=int(request.POST.get("paymenttype"))
                if int(request.session.get("uid"))!=int(uid):
                    data={}
                    data['status']="failed"
                    data['message']=MESSAGE.INVALID_USERID
                    return JsonResponse(data)
                purchases=Purchases.objects.filter(Q(uid=uid) & Q(pid = productid)).all()
                if len(purchases)>0:
                    data={}
                    data['status']="ok"
                    data['message']=MESSAGE.ITEM_PURCHASED
                    p=Product.objects.filter(id=productid).all()
                    contentid=p[0].contentid
                    content=Content.objects.filter(identifier=contentid).all()
                    c=content[0]
                    p=p[0]
                    purchase=purchases[0]
                    author = Author.objects.get(id=p.authorid)
                    purchasedata=getPurchaseDict(p,purchase,c,author)
                    data['products']=purchasedata
                    try:
                        title=p.name
                        contentid=str(p.id)
                        likes=0
                        listen=0
                        download=0
                        c=ContentRating.objects(contentid=contentid,uid=uid)
                        print "fetching from mongo ",c
                        if c.count()<=0:
                            download=download+1
                            c=ContentRating(contentid =contentid ,uid=uid,like=likes,listen=listen,download=download,title =title ,createdate = timezone.now())
                            c.save()
                        else:
                            download=int(c[0].download)+1
                            c[0].update(download=download)

                    except Exception as ex:
                        print ex
                    return JsonResponse(data)
                uid=request.session.get("uid")
                product=Product.objects.filter(Q(id=productid)).all()
                purchaseamount=int(product[0].price)
                if paymenttype==1:
                    print "Got here"
                    wallet=Wallet.objects.filter(Q(uid=uid)).all()
                    currentbalance=int(wallet[0].balance)
                    print "user balance ",currentbalance
                    print "amount ",purchaseamount
                    if currentbalance<purchaseamount:
                        data={}
                        data['status']="failed"
                        data['message']=MESSAGE.INSUFFICIENT_FUNDS
                        return JsonResponse(data)
                    newbalance=currentbalance-purchaseamount
                    wallet.update(balance=newbalance)
                    comment=""
                    status=1
                    purchase=Purchases.objects.create(uid=uid,pid = productid,comment = comment,
                    amount =purchaseamount ,tax = 0.0,commission = 0.0, status = status,
                    createdate =timezone.now())
                    #this should return the info about the purchase
                    #the license key
                    #the secret key
                    print "Product ID ",productid
                    product=Product.objects.filter(id=productid).all()
                    contentid=product[0].contentid
                    content=Content.objects.filter(identifier=contentid).all()
                    c=content[0]
                    p=product[0]
                    author = Author.objects.get(id=p.authorid)
                    purchasedata=getPurchaseDict(p,purchase,c,author)
                    print purchasedata
                    data={}
                    data['products']=purchasedata
                    data['status']="ok"
                    data['message']=MESSAGE.PURCHASE_SUCCESS
                else:
                    data={}
                    data['status']="ok"
                    data['message']=MESSAGE.PAYMENT_UNSUPPORTED
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']=MESSAGE.PURCHASE_FAIL
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

@csrf_exempt
def getpurchases(request):
    if request.session.get('isloggedin', False):
        print "Starting here"
        if request.method == "POST":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            print "Ready"

            try:
                print "Get data"
                uid=request.POST.get("uid")
                print uid
                purchase=Purchases.objects.raw("select a.id,b.name as name,d.name as author,b.price,b.adddate,a.createdate as purchasedate,b.description,b.contentid,c.filename,c.url,c.defaultkey,c.size from api_purchases a,api_product b,api_content c,api_author d where d.id=b.authorid and a.pid=b.id and b.contentid=c.id and a.uid="+uid)
                purchasedata=getPurchasesDict(purchase)
                print purchasedata
                data={}
                data['products']=purchasedata
                data['status']="ok"
                data['message']=MESSAGE.PURCHASE_SUCCESS
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']=MESSAGE.PURCHASE_FAIL
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
