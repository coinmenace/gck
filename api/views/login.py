from imports import *
from django.contrib.gis.geoip import GeoIP

#login new account
#@csrf_protect
@csrf_exempt
def login(request):
    if request.session.get('isloggedin', False):

        return JsonResponse(data)
    else:
        return JsonResponse(data)


#authenticate user
#@csrf_protect
@csrf_exempt
def auth(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        username=request.POST.get("username")
        passwd=request.POST.get("password")
        device=[]
        password=hashlib.sha256(passwd).hexdigest()
        currentuser={}
        try:
            ipaddress = get_client_ip(request)
            print ipaddress
            g = GeoIP()
            cityinfo = g.city(ipaddress)
            print cityinfo
        except Exception as ex:
            print ex
        try:
            appversion = request.META['HTTP_RT_APP_VERSION']
            deviceos = request.META['HTTP_RT_DEVICE_OS']
            devicetype = request.META['HTTP_RT_DEVICE_TYPE']
            ua = request.META['HTTP_USER_AGENT']
            deviceid = request.META['HTTP_RT_DEVICE_ID']
            devicename = devicetype
            devicefullname = devicetype + "_" + deviceos + "_" + appversion + "_" + ua
        except Exception as ex:
            print ex
            devicename = "Unknown"
            devicefullname = "Unknown" + "_" + "Unknown" + "_" + "v0.7.1" + "_" + "mobile"
            #data = {}
            #data['message'] = "invalid headers"
            #data['status'] = "failed"
            #return JsonResponse(data)


        try:
            # User.objects.filter(Q(username=username) &Q(password=password))
            print username,password,deviceid
            userobject=User.objects.filter(Q(username=username) &Q(password=password)).get()
            if userobject.username==username:
                uid=userobject.id

                #check if device is blacklisted
                blacklisted = None
                try:
                    blacklisted = rdb.get("blacklisted_devices_" + str(uid))

                    if blacklisted:
                        device = json.loads(blacklisted)
                        print device,deviceid
                        if device['device']==deviceid:
                            data = {}
                            data['message'] = "Unfortunately this device has been blacklisted by "+username+".If this is an error,Kindly contact support at support@ridit.com to fix this."
                            data['status'] = "failed"
                            return JsonResponse(data)
                except Exception as ex:
                    print ex
                currentuser['uid']=uid
                currentuser['username']=userobject.username
                currentuser['secret']=userobject.secret
                profileobject = Profile.objects.filter(Q(uid=currentuser['uid'])).get()
                currentuser['firstname']=profileobject.firstname
                currentuser['lastname']=profileobject.lastname
                currentuser['email']=profileobject.email
                currentuser['profilepics']=profileobject.profilepics
                currentuser['biography']=profileobject.biography
                currentuser['telephone']=profileobject.telephone
                currentuser['pid']=profileobject.id
                wallet = Wallet.objects.filter(Q(uid=currentuser['uid'])).get()
                currentuser['balance']=wallet.balance
                currentuser['wid']=wallet.id
                currentuser['purchaseurl'] = settings.siteurl+"/api/v1/purchase"
                currentuser['paymenturl'] = settings.siteurl + "/api/v1/payment"
                currentuser['voucherurl'] = settings.siteurl + "/api/v1/voucher/gift"
                data={}
                data['message']=MESSAGE.LOGIN_SUCCESS
                try:
                    #deviceid=request.POST.get("deviceid")
                    device=Device.objects.get(uid=uid)
                    print "Length of records ", len(device)
                    if len(device) > 0:
                        if device[0].uuid != deviceid:
                            data['requireswipe'] = True
                except Exception as ex:
                    print ex
                    try:
                        if len(device) <= 0:
                            print deviceid
                            Device.objects.create(name=devicename,fullname=devicefullname,uid=uid, uuid=deviceid, createdate=timezone.now())
                    except Exception as e:
                        print e
                data['requiresupdate']=0
                data['status']="ok"
                data['user']=currentuser
                request.session['isloggedin'] =True
                request.session['uid'] =userobject.id
                try:
                    #request.session['sessionhash'] =uid:
                    # check for active user
                    # using uid,deviceid,sessionid
                    sessionid = request.session._session_key
                    print uid, deviceid, sessionid
                    userdata = checkActiveUser(uid, deviceid, sessionid)
                    print userdata
                    try:
                        if userdata['requires_verification']:
                            recipient = convertToInternationalNumber(profileobject.telephone)
                            print recipient
                            code = get2FACode()
                            request.session['uid'] = uid
                            request.session['2fa'] = code
                            message = "Kindly verify your account with the following verification token: " + str(code)
                            sendMessage(recipient, message)
                    except Exception as ex:
                        print ex
                    data['session_changed'] = userdata['session_changed']
                    data['requires_verification'] = userdata['requires_verification']
                except Exception as ex:
                    print ex
            else:
                data={}
                data['message']=MESSAGE.LOGIN_FAIL
                data['status']="failed"
        except Exception as ex:
            print ex
            data={}
            data['message']=MESSAGE.LOGIN_FAIL
            data['status']="failed"


        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.INVALID_REQUEST_POST
        data['status']="failed"
        return JsonResponse(data)






#reset password
#@csrf_protect
@csrf_exempt
def resetpass(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        emailorphone=request.POST.get("emailorphone")
        try:
            # User.objects.filter(Q(username=username) &Q(password=password))
            profileobject=Profile.objects.filter(Q(email=emailorphone) | Q(telephone=emailorphone)).get()
            if profileobject !=None :
                uid = profileobject.uid
                userobject = User.objects.get(id=uid)
                passwd = generateTempPassword()
                password = hashlib.sha256(passwd).hexdigest()
                userobject.password = passwd
                userobject.save()
                data['status']="ok"
                data['message']="successfully reset password"

            else:
                data={}
                data['message']="unable to reset password"
                data['status']="failed"
        except Exception as ex:
            print ex
            data={}
            data['message']="unable to reset password"
            data['status']="failed"

        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.INVALID_REQUEST_POST
        data['status']="failed"
        return JsonResponse(data)





#change password
#@csrf_protect
@csrf_exempt
def changepass(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        uid=request.POST.get("uid")
        passwd=request.POST.get("password")
        device=[]
        password=hashlib.sha256(passwd).hexdigest()
        currentuser={}
        try:
            ipaddress = get_client_ip(request)
            print ipaddress
            g = GeoIP()
            cityinfo = g.city(ipaddress)
            print cityinfo
        except Exception as ex:
            print ex
        try:
            appversion = request.META['HTTP_RT_APP_VERSION']
            deviceos = request.META['HTTP_RT_DEVICE_OS']
            devicetype = request.META['HTTP_RT_DEVICE_TYPE']
            ua = request.META['HTTP_USER_AGENT']
            deviceid = request.META['HTTP_RT_DEVICE_ID']
            devicename = devicetype
            devicefullname = devicetype + "_" + deviceos + "_" + appversion + "_" + ua
        except Exception as ex:
            print ex
            devicename = "Unknown"
            devicefullname = "Unknown" + "_" + "Unknown" + "_" + "v0.7.1" + "_" + "mobile"
        try:
            # User.objects.filter(Q(username=username) &Q(password=password))
            userobject=User.objects.filter(Q(id=uid)).get()
            if userobject.id ==uid:
                userobject.password = passwd
                userobject.save()
                data={}
                data['message']="sucessfully changed password"
                data['status']="ok"
            else:
                data={}
                data['message']="unable to reset user password"
                data['status']="failed"
        except Exception as ex:
            print ex
            data={}
            data['message']="unable to reset user password"
            data['status']="failed"

        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.INVALID_REQUEST_POST
        data['status']="failed"
        return JsonResponse(data)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def multiverifydevice(request):
    if request.method == "POST":
        response=verifySignature(request)
        try:
            appversion = request.META['HTTP_RT_APP_VERSION']
            deviceos = request.META['HTTP_RT_DEVICE_OS']
            devicetype = request.META['HTTP_RT_DEVICE_TYPE']
            ua = request.META['HTTP_USER_AGENT']
            deviceid = request.META['HTTP_RT_DEVICE_ID']
            devicename = devicetype
            devicefullname = devicetype + "_" + deviceos + "_" + appversion + "_" + ua
        except Exception as ex:
            print ex
        if response['status']=="failed":
            return JsonResponse(response)
        code=request.POST.get("code")
        print "Code sent is "+code
        securecode=request.session['2fa']
        print "Session saved code is "+str(securecode)
        sessionid = request.session._session_key
        if str(securecode)==code:
            if "uid" in request.session:
                uid=request.session['uid']
                user=User.objects.get(id=uid)
                user.isphoneverified=1
                user.save()
                try:
                    device = Device.objects.filter(Q(uid=uid))[0]
                    olddeviceid = device.uuid
                    device.name = devicename
                    device.fullname = devicefullname
                    device.uuid = deviceid
                    device.createdate = timezone.now()
                    device.save()
                    blacklisteduserdata = {'uid': uid, 'device': olddeviceid}
                    blacklisted = json.dumps(blacklisteduserdata)
                    print "blacklisted_devices_"+str(uid),blacklisted
                    print "blacklisted_devices",blacklisted
                    rdb.set("blacklisted_devices_"+str(uid),blacklisted)
                    rdb.lpush("blacklisted_devices",blacklisted)

                except Exception as ex:
                    print ex
                    device =  Device.objects.create(name=devicename, fullname=devicefullname, uid=uid, uuid=deviceid,createdate=timezone.now())
            userkey = "user_" + str(uid)
            savedkey = rdb.get(userkey)
            if savedkey:
                try:
                    jsondata = str(savedkey).replace('u\'', '\'').replace('\'', '"')
                    print jsondata
                    userdata = json.loads(jsondata)
                    userdata['device'] = deviceid
                    userdata['sessionid'] = sessionid
                    rdb.set(userkey, userdata)
                except Exception as ex:
                    print ex
            else:
                userdata = {'uid': uid, 'device': deviceid, 'sessionid': sessionid}
                userdata = json.dumps(userdata)
                print userdata
                rdb.set(userkey, userdata)
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

