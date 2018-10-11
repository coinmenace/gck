from imports import *

def createcategory(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            category=processCategory(name)
            if category.id!=None:
                data={}
                data['status'] = "ok"
                data['message'] = "category created successfully"
            else:
                data={}
                data['message'] = "unable to create category"
                data['status'] = "failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../content")
        else:
            data={}
            data['message'] = "invalid method POST required"
            data['status'] = "failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../content")

    else:
        data={}
        data['message'] = "admin not loggedin"
        data['status'] = "failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")

def updatecategory(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            categoryid = request.POST.get("categoryid")
            name=request.POST.get("name")
            category=processCategory(name,categoryid)
            if category.id!=None:
                data={}
                data['status']="ok"
                data['message']="category updated successfully"
            else:
                data={}
                data['message']="unable to update category"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../content")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../content")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def listcategory(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        #media=Category.objects.all()
        media = getSubCategory()
        data={}
        data['total']= Category.objects.count()
        data['rows']=categoryToJson(media)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deletecategory(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            categoryid=request.GET['id']
        else:
            categoryid=id
        category=Category.objects.get(id=categoryid)
        category.delete()
        return HttpResponseRedirect("../../content")
    else:
        return HttpResponseRedirect("login")


def processCategory(name,categoryid=None):
    if categoryid == None:
        category = Category.objects.create(name=name, createdate=timezone.now())
    else:
        category = Category.objects.get(id = categoryid)
        category.name = name
        category.save()
    return category


def createsubcategory(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            categoryid = request.POST.get("categoryid")
            print request.POST
            category=processSubCategory(name,categoryid)
            if category.id!=None:
                data={}
                data['status'] = "ok"
                data['message'] = "subcategory created successfully"
            else:
                data={}
                data['message'] = "unable to create subcategory"
                data['status'] = "failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../content")
        else:
            data={}
            data['message'] = "invalid method POST required"
            data['status'] = "failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../content")

    else:
        data={}
        data['message'] = "admin not loggedin"
        data['status'] = "failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")

def updatesubcategory(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            categoryid = request.POST.get("categoryid")
            subcategoryid = request.POST.get("subcategoryid")
            name=request.POST.get("name")
            category=processSubCategory(name,categoryid,subcategoryid)
            if category.id!=None:
                data={}
                data['status']="ok"
                data['message']="subcategory updated successfully"
            else:
                data={}
                data['message']="unable to update subcategory"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../content")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../content")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def listsubcategory(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        media=getSubCategory()
        data={}
        data['total']= SubCategory.objects.count()
        data['rows']=subCategoryToJson(media)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deletesubcategory(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            subcategoryid=request.GET['id']
        else:
            subcategoryid=id
        category=SubCategory.objects.get(id=subcategoryid)
        category.delete()
        return HttpResponseRedirect("../../content")
    else:
        return HttpResponseRedirect("login")


def processSubCategory(name,categoryid=None,subcategoryid=None):
    print name,categoryid,subcategoryid
    if subcategoryid==None:
        category = SubCategory.objects.create(name=name,categoryid=categoryid, createdate=timezone.now())
    else:
        category = SubCategory.objects.get(name = name)
        category.name = name
        category.save()
    return category


def getSubCategory():
    subcategory = SubCategory.objects.raw("SELECT a.id as id,a.name as catname,a.createdate as catdate,b.id as subcatid,b.name as subcatname,b.createdate as subcatdate from api_category as a LEFT JOIN api_subcategory as b ON  b.categoryid=a.id")
    return subcategory