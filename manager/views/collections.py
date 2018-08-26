from imports import *



def createcollection(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            description=request.POST.get("description")
            collection=processCollection(name,description)
            if collection.id!=None:
                data={}
                data['status']="ok"
                data['message']="collection created successfully"
            else:
                data={}
                data['message']="unable to create collection"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../books")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../books")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")

def updatecollection(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            collectionid = request.POST.get("collectionid")
            name=request.POST.get("name")
            description=request.POST.get("description")
            collection=processCollection(name,description,collectionid)
            if collection.id!=None:
                data={}
                data['status']="ok"
                data['message']="collection updated successfully"
            else:
                data={}
                data['message']="unable to update collection"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../books")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../books")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def deletecollection(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            collectionid=request.GET['id']
        else:
            collectionid=id
        collection=Collection.objects.get(id=collectionid)
        collection.delete()
        return HttpResponseRedirect("../../books")
    else:
        return HttpResponseRedirect("login")


def processCollection(name,description,collectionid=None):
    if collectionid == None:
        collection = Collection.objects.create(name=name, description=description, createdate=timezone.now())
    else:
        collection = Collection.objects.get(id =  collectionid)
        collection.name  = name
        collection.description = description
        collection.save()
    return collection

