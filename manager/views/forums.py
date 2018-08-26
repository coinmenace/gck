from imports import *



def forums(request):
    if request.session.get('isloggedin', False):
        data['view']="forums"
        data['username']=request.session.get("username")
        data['forumtopic']=ForumTopic.objects.all()
        template = loader.get_template('manager_forum.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")



def listforums(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        forum=ForumTopic.objects.raw("SELECT  api_forumtopic.id as id,topic,comments,likes,isactive,api_forumtopic.createdate as createdate from api_forumtopic "+pager)
        data={}
        data['total']=  ForumTopic.objects.count()
        data['rows']=forumToJson(forum)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deleteforums(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            forumid=request.GET['id']
        else:
            forumid=id
        forum=ForumTopic.objects.get(id=forumid)
        forum.delete()
        return HttpResponseRedirect("../../forums")
    else:
        return HttpResponseRedirect("login")


def createforumtopic(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            topic=request.POST.get("topic")
            body=request.POST.get("body")
            poster=request.FILES["image"]
            filename=poster.name
            thumbid=generatethumbs(poster)
            uid=request.session.get("uid")
            forumtopic=processForum(topic,body,thumbid,uid,forumid=None)
            if forumtopic.id!=None:
                data={}
                data['status']="ok"
                data['message']="forumtopic created successfully"
            else:
                data={}
                data['message']="unable to create forumtopic"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../forums")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../forums")
    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")



def updateforumtopic(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            forumid = request.POST.get("forumid")
            topic=request.POST.get("topic")
            body=request.POST.get("body")
            poster=request.FILES["image"]
            filename=poster.name
            thumbid=generatethumbs(poster)
            uid=request.session.get("uid")
            forumtopic=processForum(topic,body,thumbid,uid,forumid=forumid)
            if forumtopic.id!=None:
                data={}
                data['status']="ok"
                data['message']="forumtopic updated successfully"
            else:
                data={}
                data['message']="unable to update forumtopic"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../forums")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../forums")
    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def processForum(topic,body,thumbid,uid,forumid=None):
    if forumid == None:
        forumtopic = ForumTopic.objects.create(topic=topic, body=body, image=thumbid, uid=uid,
                                               createdate=timezone.now())
    else:
        forumtopic = ForumTopic.objects.get(id= forumid)
        forumtopic.topic = topic
        forumtopic.body = body
        forumtopic.image = thumbid
        forumtopic.uid = uid
        forumtopic.save()
    return forumtopic