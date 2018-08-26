from imports import *


def admin(request):
    if request.session.get('isloggedin', False):
        data['username']=request.session.get("username")
        data['view']="admin"
        adminrole=AdminRole.objects.all()
        data['role']=adminrole
        if "editadmin" in data:
            del data['editadmin']
        template = loader.get_template('manager_admin.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def createadmin(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            username=request.POST.get("username")
            passwd=request.POST.get("password")
            secret=hashlib.md5(passwd).hexdigest()
            role=request.POST.get("role")
            password=hashlib.sha256(passwd).hexdigest()
            verifyuser={}
            user={}
            user['id']=None
            verifyuser['username']=None
            try:
                userobject=Admin.objects.filter(Q(username=username)).get()
                verifyuser['username']=userobject.username
            except Exception as ex:
                print ex
            if verifyuser['username']==None:
                status=1
                user=Admin.objects.create(username=username,password=password,role=role,secret=secret,status=status,createdate=timezone.now())
                if user.id!=None:
                    uid=user.id
                    data={}
                    data['uid']=uid
                    data['username']=username
                    data['status']="ok"
                    data['message']="admin user created successfully"
                else:
                    data={}
                    data['message']="unable to create admin user"
                    data['status']="failed"
            else:
                data={}
                data['message']="admin user with this username exists"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("/manager/admin")
        else:
            data={}
            data['message']="admin user with this username exists"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/admin")

    else:
        data={}
        context = {
        'data': data
        }
        return HttpResponseRedirect("../login")

def createadminrole(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            role=AdminRole.objects.create(name=name,createdate=timezone.now())
            if role.id!=None:
                data={}
                data['status']="ok"
                data['message']="admin role created successfully"
            else:
                data={}
                data['message']="unable to create admin role"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../admin")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../admin")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def viewadmin(request,id):
    if request.session.get('isloggedin', False):
        data['view']="users"
        admin=Admin.objects.get(id=id)
        role=AdminRole.objects.all()
        data['admin']=admin
        data['role']=role
        data['editadmin']=True
        template = loader.get_template('manager_admin.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")



def updateadmin(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            print "Update admin"
            username=request.POST.get("username")
            passwd=request.POST.get("password")
            secret=hashlib.md5(passwd).hexdigest()
            role=request.POST.get("role")
            password=hashlib.sha256(passwd).hexdigest()
            verifyuser={}
            user={}
            user['id']=None
            admin=Admin.objects.get(username=username)
            if passwd!=None and passwd!="":
                admin.password=password
            admin.role=role
            admin.save()
            return HttpResponseRedirect("/manager/admin")
        else:
            data={}
            data['message']="admin user with this username exists"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/admin")

    else:
        data={}
        context = {
        'data': data
        }
        return HttpResponseRedirect("../login")


def listadmin(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        admin=Admin.objects.raw("SELECT  api_admin.id as id,api_adminrole.name as role,username,status from api_admin,api_adminrole WHERE api_admin.role=api_adminrole.id "+pager)
        data={}
        data['total']= Admin.objects.count()
        data['rows']=adminToJson(admin)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deleteadmin(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            adminid=request.GET['id']
        else:
            adminid=id
        admin=Admin.objects.get(id=adminid)
        admin.delete()
        return HttpResponseRedirect("../../admin")
    else:
        return HttpResponseRedirect("login")
