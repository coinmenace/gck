from imports import *

@csrf_exempt
def dolike(request,mediaid):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        if mediaid == None:
            contentid=request.POST.get("mediaid")
        else:
            contentid = mediaid
        uid=request.session['uid']
        p = Product.objects.filter(id=contentid).all()
        title=p[0].name
        likes=0
        listen=0
        download=0
        c=ContentRating.objects(contentid=contentid,uid=uid)
        if c.count()<=0:
            likes=1
            c=ContentRating(contentid =contentid ,uid=uid,like=likes,listen=listen,download=download,title =title ,createdate = timezone.now())
            c.save()
        else:
            likes=1
            c[0].update(likes=likes)
        if True:
            data={}
            data['message']=MESSAGE.VERIFY_OK
            data['status']="ok"
            return JsonResponse(data)
        else:
            data={}
            data['message']=MESSAGE.VERIFY_FAILED_INVALIDCODE
            data['status']="failed"
            return JsonResponse(data)

    else:
        data={}
        data['message']=MESSAGE.LIKE_FAILED
        data['status']="failed"
        return JsonResponse(data)


@csrf_exempt
def dounlike(request,mediaid):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        if mediaid == None:
            contentid=request.POST.get("mediaid")
        else:
            contentid = mediaid
        uid=request.session['uid']
        p = Product.objects.filter(id=contentid).all()
        title=p[0].name
        likes=0
        listen=0
        download=0
        c=ContentRating.objects(contentid=contentid,uid=uid)
        if c.count()<=0:
            likes=0
            c=ContentRating(contentid =contentid ,uid=uid,like=likes,listen=listen,download=download,title =title ,createdate = timezone.now())
            c.save()
        else:
            likes=0
            c[0].update(likes=likes)
        if True:
            data={}
            data['message']=MESSAGE.VERIFY_OK
            data['status']="ok"
            return JsonResponse(data)
        else:
            data={}
            data['message']=MESSAGE.VERIFY_FAILED_INVALIDCODE
            data['status']="failed"
            return JsonResponse(data)

    else:
        data={}
        data['message']=MESSAGE.LIKE_FAILED
        data['status']="failed"
        return JsonResponse(data)


@csrf_exempt
def dolisten(request,mediaid):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        if mediaid == None:
            contentid=request.POST.get("mediaid")
        else:
            contentid = mediaid
        uid=request.session['uid']
        p = Product.objects.filter(id=contentid).all()
        print p
        title=p[0].name
        likes=0
        listen=0
        download=0
        c=ContentRating.objects(contentid=contentid,uid=uid)
        if c.count()<=0:
            listen=1
            c=ContentRating(contentid =contentid ,uid=uid,like=likes,listen=listen,download=download,title =title ,createdate = timezone.now())
            c.save()
        else:
            clisten = c[0].listen
            listen=clisten + 1
            c[0].update(listen=listen)
        if True:
            data={}
            data['message']=MESSAGE.VERIFY_OK
            data['status']="ok"
            return JsonResponse(data)
        else:
            data={}
            data['message']=MESSAGE.VERIFY_FAILED_INVALIDCODE
            data['status']="failed"
            return JsonResponse(data)

    else:
        data={}
        data['message']="unable to update listens"
        data['status']="failed"
        return JsonResponse(data)