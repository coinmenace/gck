from imports import *

def authors(request):
    if request.session.get('isloggedin', False):
        print "Authors"
        data['view']="authors"
        data['username']=request.session.get("username")
        authors=Author.objects.all()
        data['authors']=authors
        template = loader.get_template('manager_authors.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def listauthors(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        authors=Author.objects.raw("SELECT  api_author.id as id,image_256X256 as image,name,joindate from api_author  left join api_thumbs on  api_author.thumbid =api_thumbs.id "+pager)
        data={}
        data['total']=  Author.objects.count()
        data['rows']=authorsToJson(authors)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deleteauthors(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            authorid=request.GET['id']
        else:
            authorid=id
        author=Author.objects.get(id=authorid)
        author.delete()
        return HttpResponseRedirect("/manager/authors")
    else:
        return HttpResponseRedirect("login")


def createauthor(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            uid=request.POST.get("uid")
            poster=request.FILES["picture"]
            filename=poster.name
            thumbid=generatethumbs(poster)
            author=processAuthor(name,thumbid[0])
            if author.id!=None:
                data={}
                data['status']="ok"
                data['message']="author created successfully"
            else:
                data={}
                data['message']="unable to create author"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("/manager/authors")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/authors")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def updateauthor(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            authorid = request.POST.get("authorid")
            name=request.POST.get("name")
            thumbid = None
            if "picture" in request.FILES:
                poster=request.FILES["picture"]
                filename=poster.name
                thumbid=generatethumbs(poster)
            author=processAuthor(name,thumbid,authorid)
            if author.id!=None:
                data={}
                data['status']="ok"
                data['message']="author updated successfully"
            else:
                data={}
                data['message']="unable to update author"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("/manager/authors")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/authors")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")

def processAuthor(name,thumbid,authorid=None):
    if authorid==None:
        author = Author.objects.create(name=name, thumbid=thumbid, joindate=timezone.now())
    else:
        author = Author.objects.get(id=authorid)
        if name!=None:
            author.name = name
            if thumbid!=None:
                author.thumbid = thumbid
            author.save()
    return author