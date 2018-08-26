from imports import *


#list authors
#@csrf_protect
@csrf_exempt
def listforums(request):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            print "List Forums"
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                #forumtopic=ForumTopic.objects.all()
                query="select a.id as id,topic,body,image_512X512 as image,comments,likes,a.createdate as postdate from api_forumtopic a,api_thumbs b where a.image=b.id"
                forumtopic=ForumTopic.objects.raw(query)
                forumlist=topicsToJsonMobile(siteurl,forumtopic)
                data={}
                data['topics']=forumlist
                data['status']="ok"
                data['message']=MESSAGE.FORUM_SUCCESS
                print data
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']=MESSAGE.FORUM_FAIL
            return JsonResponse(data)
        else:
            data={}
            data['status']="failed"
            data['message']=MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']=MESSAGE.INVALID_SESSION
        return JsonResponse(data)


#@csrf_protect
@csrf_exempt
def postcomment(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        topicid=request.POST.get("topicid")
        uid=request.POST.get("uid")
        message=request.POST.get("message")
        post=ForumPost.objects.create(uid=uid,body=message,topicid=topicid,isactive=1,createdate=timezone.now())
        data={}
        if post.id!=None:
            data['status']="ok"
            data['message']=MESSAGE.POST_SUCCESS
            data['postid']=post.id
        else:
            data['status']="failed"
            data['message']=MESSAGE.POST_FAILED


        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        return JsonResponse(data)


@csrf_exempt
def listpost(request,topic,page):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            print "List Forum Post"
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                if not topic:
                    topicid=str(request.GET.get("topic"))
                else:
                    topicid=str(topic)
                if not page:
                    page=int(request.GET.get("page"))
                else:
                    page=int(page)
                offset=str(page*20)
                limit="20"
                pager="LIMIT "+offset+","+limit
                query="select api_forumpost.id as id,api_forumpost.uid,username,topic,api_forumpost.body,api_forumpost.comments as comments,api_forumpost.likes as likes,api_forumpost.createdate as postdate from api_user,api_forumpost,api_forumtopic where api_user.id=api_forumpost.uid and api_forumpost.topicid=api_forumtopic.id and  api_forumtopic.id="+topicid
                forumpost=ForumPost.objects.raw(query)
                forumlist=postToJsonMobile(forumpost)
                data={}
                data['topics']=forumlist
                data['status']="ok"
                data['message']=MESSAGE.FORUM_POST_SUCCESS
                print data
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']=MESSAGE.FORUM_POST_FAIL
            return JsonResponse(data)
        else:
            data={}
            data['status']="failed"
            data['message']=MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']=MESSAGE.INVALID_SESSION
        return JsonResponse(data)
