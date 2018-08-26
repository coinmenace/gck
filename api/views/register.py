from imports import *
#register new account
#@csrf_protect
@csrf_exempt
def registeruser(request):
    if request.method == "POST":
        print MESSAGE
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        username=request.POST.get("username")
        passwd=request.POST.get("password")
        telephone=request.POST.get("telephone")
        email=request.POST.get("email")
        secret=hashlib.md5(passwd).hexdigest()
        password=hashlib.sha256(passwd).hexdigest()
        verifyuser={"username":None}
        verifyprofile={"email":None,"telephone":None}
        print email,telephone,username
        #recharge new accounts 100 naira
        balance=100.0
        try:
            userobject=User.objects.filter(Q(username=username)).get()
            verifyuser['username']=userobject.username
        except Exception as ex:
            print ex
        try:
            profileobject=Profile.objects.filter(Q(email=email) | Q(telephone=telephone)).get()
            verifyprofile['email']=profileobject.email
            verifyprofile['telephone']=profileobject.telephone
        except Exception as ex:
            print ex
        print verifyprofile
        print verifyuser
        if verifyprofile['email']!=None and verifyprofile['email']==email:
            data={}
            data['message']=MESSAGE.EMAIL_EXISTS
            data['status']="failed"
        elif verifyprofile['telephone']!=None and verifyprofile['telephone']==telephone:
            data={}
            data['message']=MESSAGE.PHONE_EXISTS
            data['status']="failed"
        elif verifyuser['username']==None:
            user=User.objects.create(username=username,password=password,secret=secret,createdate=timezone.now())
            if user.id!=None:
                uid=user.id
                profile=Profile.objects.create(uid=uid,email=email,telephone=telephone,createdate=timezone.now())
                wallet=Wallet.objects.create(uid=uid,balance=balance,createdate=timezone.now())
                data={}
                data['uid']=uid
                data['username']=username
                data['status']="ok"
                if settings.requires2fa:
                    data['verify']=1
                else:
                    data['verify']=0
                data['message']=MESSAGE.CREATE_USER_SUCCESS
                recipient = convertToInternationalNumber(profile.telephone)
                code=get2FACode()
                request.session['uid']=uid
                request.session['2fa']=code
                message= "Thank you for signing up for "+settings.SITENAME+". Your verification token is: "+str(code)
                sendMessage(recipient,message)
            else:
                data={}
                data['message']=MESSAGE.UNABLE_TO_CREATE
                data['status']="failed"
        else:
            data={}
            data['message']=MESSAGE.USER_EXISTS
            data['status']="failed"

        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        return JsonResponse(data)

@csrf_exempt
def verifydevice(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        code=request.POST.get("code")
        print "Code sent is "+code
        securecode=request.session['2fa']
        print "Session saved code is "+str(securecode)
        if str(securecode)==code:
            if "uid" in request.session:
                uid=request.session['uid']
                user=User.objects.get(id=uid)
                user.isphoneverified=1
                user.save()
            data={}
            data['message']=MESSAGE.VERIFY_OK
            data['status']="ok"
            data['uid']=uid
            return JsonResponse(data)
        else:
            data={}
            data['message']=MESSAGE.VERIFY_FAILED_INVALIDCODE
            data['status']="failed"
            return JsonResponse(data)

    else:
        data={}
        data['message']=MESSAGE.VERIFY_FAILED
        data['status']="failed"
        return JsonResponse(data)

#register device
#@csrf_protect
@csrf_exempt
def registerdevice(request):
    if request.session.get('isloggedin', False):

        return JsonResponse(data)
    else:
        return JsonResponse(data)

