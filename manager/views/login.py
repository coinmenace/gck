from imports import *

def login(request):
    template = loader.get_template('manager_login.html')
    data['view']="login"
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))

def logout(request):
    	for key in request.session.keys():
		del request.session[key]
	request.session.modified = True
	return HttpResponseRedirect("login")


def auth(request):
    if request.method == "POST":
            username=request.POST.get("username")
            passwd=request.POST.get("password")
            password=hashlib.sha256(passwd).hexdigest()
            try:
                admin=Admin.objects.filter(Q(username=username) & Q(password=password)).get()
                if admin.username!=None:
                    data={}
                    request.session['isloggedin']=True
                    request.session['username']=username
                    request.session['uid']=admin.id
                    request.session['role']=admin.role
                    request.session['message']=""
                    print request.session
                    return HttpResponseRedirect("/manager")

                else:
                    request.session['isloggedin']=False
                    request.session['message'] ="Invalid username/password."
                    print request.session
                    return HttpResponseRedirect("login")
            except Exception as ex:
                print ex
                request.session['isloggedin']=False
                request.session['message'] = "Error:"+str(ex)
                print request.session
                return HttpResponseRedirect("login")



    else:
        request.session['isloggedin']=False
        request.session['message'] = "Invalid method.POST required"
        return HttpResponseRedirect("login")