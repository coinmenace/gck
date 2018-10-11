from imports import *


def users(request):
    if request.session.get('isloggedin', False):
        data['username']=request.session.get("username")
        data['view']="users"
        adminrole=AdminRole.objects.all()
        data['role']=adminrole
        if "edit" in data:
            del data['edit']
        if "editpass" in data:
            del data['editpass']
        template = loader.get_template('manager_users.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def vieweditpassword(request,id):
    if request.session.get('isloggedin', False):
        data['view']="users"
        user=User.objects.get(id=id)
        data['user']=user
        data['editpass']=True
        template = loader.get_template('manager_users.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")



def vieweditusers(request,id):
    if request.session.get('isloggedin', False):
        data['view']="users"
        query="SELECT a.id as id,b.firstname,b.lastname,b.email,b.telephone,b.address1,b.address2 FROM api_user a,api_profile b WHERE a.id=b.uid AND a.id="+str(id)
        user=User.objects.raw(query)
        data['user']=user[0]
        data['edit']=True
        template = loader.get_template('manager_users.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")



def createuser(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username=request.POST.get("username")
        passwd=request.POST.get("password")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        telephone=request.POST.get("telephone")
        email=request.POST.get("email")
        secret=hashlib.md5(passwd).hexdigest()
        password=hashlib.sha256(passwd).hexdigest()
        verifyuser={"username":None}
        verifyprofile={"email":None,"telephone":None}
        print email,telephone,username
        balance=0.0
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
            request.session['message']="account with this email exists"
            request.session['status']="failed"
        elif verifyprofile['telephone']!=None and verifyprofile['telephone']==telephone:
            data={}
            request.session['message']="account with this phone exists"
            request.session['status']="failed"
        elif verifyuser['username']==None:
            phoneverified=1
            user=User.objects.create(username=username,password=password,secret=secret,isphoneverified=phoneverified,createdate=timezone.now())
            if user.id!=None:
                uid=user.id
                #city=city,state=state,country=country,
                profile=Profile.objects.create(firstname=firstname,lastname=lastname,address1=address,uid=uid,email=email,telephone=telephone,createdate=timezone.now())
                wallet=Wallet.objects.create(uid=uid,balance=balance,createdate=timezone.now())
                request.session['message']="account created successfully"
                request.session['status']="ok"
            else:
                data={}
                request.session['message']="unable to create user"
                request.session['status']="failed"
        else:
            data={}
            request.session['message']="account exists"
            request.session['status']="failed"

        return HttpResponseRedirect("../users")
    else:
        data={}
        request.session['message']="account exists"
        request.session['status']="failed"
        return HttpResponseRedirect("../login")




def updateuser(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            firstname=request.POST.get("firstname")
            lastname=request.POST.get("lastname")
            username=request.POST.get("username")
            passwd = request.POST.get("password")
            email=request.POST.get("email")
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            country = request.POST.get("country")
            telephone=request.POST.get("telephone")
            uid=request.POST.get("uid")
            secret = hashlib.md5(passwd).hexdigest()
            password = hashlib.sha256(passwd).hexdigest()
            user = User.objects.get(id=uid)
            user.username=username
            if passwd!=None and passwd!="":
                user.secret = secret
                user.password = password
            user.save()
            profile=Profile.objects.get(uid=uid)
            profile.firstname=firstname
            profile.lastname=lastname
            profile.email = email
            profile.telephone = telephone
            profile.address1 = address
            #profile.city = city
            #profile.state = state
            #profile.country = country
            profile.save()
            return HttpResponseRedirect("/manager/users")
        else:
            data={}
            request.session['message']="user with this username exists"
            request.session['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/users")

    else:
        data={}
        context = {
        'data': data
        }
        return HttpResponseRedirect("../login")

def updatepass(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            uid=request.POST.get("uid")
            username=request.POST.get("username")
            password=request.POST.get("password")
            password2=request.POST.get("password2")
            if password==password2:
                password=hashlib.sha256(password).hexdigest()
            else:
                request.session['message']="passwords do not match"
                request.session['status']="failed"
                return HttpResponseRedirect("/manager/users")
            request.session['message']="successfully changed password"
            request.session['status']="ok"
            user=User.objects.get(id=uid)
            user.password=password
            user.save()
            return HttpResponseRedirect("/manager/users")
        else:
            data={}
            request.session['message']="user with this username exists"
            request.session['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/users")

    else:
        data={}
        context = {
        'data': data
        }
        return HttpResponseRedirect("../login")


def listusers(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        users=User.objects.raw("SELECT  api_user.id as id,firstname,lastname,email,telephone,address1 as address,city,state,country,username,isphoneverified,isemailverified,status,api_user.createdate as createdate from api_user,api_profile WHERE api_user.id=api_profile.uid "+pager)
        data={}
        data['total']= User.objects.count()
        data['rows']=usersToJson(users)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deleteuser(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            userid=request.GET['id']
        else:
            userid=id
        user=User.objects.get(id=userid)
        user.delete()
        profile=Profile.objects.get(uid=userid)
        profile.delete()
        return HttpResponseRedirect("../../users")
    else:
        return HttpResponseRedirect("login")


def resetuserdevice(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            userid=request.GET['id']
        else:
            userid=id
        device=Device.objects.filter(Q(uid=userid))
        device.delete()
        rdb.delete("blacklisted_devices_" + str(userid))
        items = rdb.lrange("blacklisted_devices",0,-1)
        newlist=[]
        for item in items:
            print item
            itemdata = json.loads(item)
            if itemdata['uid']!=userid:
                newlist.append(item)
                rdb.lpush("blacklisted_devices", item)
        rdb.delete("user_" + str(userid))
        rdb.delete("blacklisted_devices")
        #rdb.lpush("blacklisted_devices",newlist)
        return HttpResponseRedirect("../../users")
    else:
        return HttpResponseRedirect("login")


def listsubscriptions(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        users=Subscriptions.objects.raw("SELECT  api_user.id as id,firstname,lastname,email,telephone,address1 as address,city,state,country,username,isphoneverified,isemailverified,status,api_user.createdate as createdate from api_user,api_profile WHERE api_user.id=api_profile.uid "+pager)
        data={}
        data['total']= Subscriptions.objects.count()
        data['rows']=usersToJson(users)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")
