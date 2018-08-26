from imports import *

#list categories
#@csrf_protect
@csrf_exempt
def getprofile(request):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
        try:
            currentuser={}
            uid=request.session.get('uid',0)
            userobject=User.objects.filter(Q(id=uid)).get()
            if userobject.id==uid:
                currentuser['uid']=userobject.id
                currentuser['username']=userobject.username
                currentuser['secret']=userobject.secret
                profileobject=Profile.objects.filter(Q(uid=currentuser['uid'])).get()
                currentuser['firstname']=profileobject.firstname
                currentuser['lastname']=profileobject.lastname
                currentuser['profilepics']=profileobject.profilepics
                currentuser['biography']=profileobject.biography
                currentuser['email']=profileobject.email
                currentuser['telephone']=profileobject.telephone
                currentuser['pid']=profileobject.id
                wallet=Wallet.objects.filter(Q(uid=currentuser['uid'])).get()
                currentuser['balance']=wallet.balance
                currentuser['wid']=wallet.id
                data={}
                data['message']=MESSAGE.LOGIN_SUCCESS
                data['requiresupdate']=0
                data['status']="ok"
                data['user']=currentuser
                request.session['isloggedin'] =True
                request.session['uid'] =userobject.id
                #request.session['sessionhash'] =uid:
            else:
                data={}
                data['message']=MESSAGE.LOGIN_FAIL
                data['status']="failed"
            return JsonResponse(data)
        except Exception as ex:
            print ex
            data={}
            data['message']=MESSAGE.LOGIN_FAIL
            data['status']="failed"
            return JsonResponse(data)
        else:
            data['status']="failed"
            data['message']=MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']=MESSAGE.INVALID_SESSION
        return JsonResponse(data)


#list categories
#@csrf_protect
@csrf_exempt
def updateprofilepicture(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            uid=request.POST.get("uid")
            poster=request.FILES["picture"]
            print poster
            filename=poster.name
            profileurl=handleprofile(poster,uid)
            profile=Profile.objects.get(uid=uid)
            if profile!=None:
                profile.profilepics=profileurl
                profile.save()
            if profile.id!=None:
                data={}
                data['status']="ok"
                data['message']="updated profile successfully"
            else:
                data={}
                data['message']="unable to update profile"
                data['status']="failed"
            return JsonResponse(data)
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            return JsonResponse(data)
        
    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        return JsonResponse(data)


def handleprofile(poster,uid):
    if not os.path.exists("website/static/profile"):
        os.mkdir("website/static/profile/")
    if not os.path.exists("tmp/"):
        os.mkdir("tmp/")
    #data=poster.read()
    #print "File size %d  ",len(data)
    with open("website/static/profile/"+str(uid)+"__"+poster.name, 'wb+') as destination:
        for chunk in poster.chunks():
            destination.write(chunk)
    #img = ImageFile(poster)
    #img.save(settings.siteurl+"/static/profile/"+str(uid)+"__"+poster.name)
    
    result={}
    return settings.siteurl+"/static/profile/"+str(uid)+"__"+poster.name
