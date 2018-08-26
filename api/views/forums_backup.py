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
                query="select a.id as id,topic,body,image_512X512 as image,comments,likes,a.createdate as postdate from api_forumtopic a,api_thumbs b where a.image=b.identifier"
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
        commenttxt=request.POST.get("message")
        image=""
        if request.FILES:
            file=request.FILES["image"]
            filename=file.name
            data=file.read()
            contentid=str(uuid.uuid4())
            print file.name
            size=[128,128]
            try:
                image=generateImages(contentid,file,filename,size)
            except Exception as ex:
                print ex
        user=User.objects.get(id=uid)
        profile=Profile.objects.get(uid=uid)
        username=user.username
        profilepic=profile.profilepics
        comment=Comment(uid=uid,topicid=topicid,text=commenttxt,username=username,profilepic=profilepic,image=image)
        comment.save()
        message=Message.objects(topicid=topicid)
        total=len(list(message))
        print "total is ",total
        status=False
        if total>0:
            print "Updating existing topic"
            #message.append(comment)
            message[0].comments.append(comment)
            message[0].save()
            status=True
        else:
            print "Inserting new topic"
            message=Message(topicid=topicid)
            message.save()
            message.comments.append(comment)
            message.save()
            status=True

        #post=ForumPost.objects.create(uid=uid,body=message,topicid=topicid,isactive=1,createdate=timezone.now())
        data={}
        if status:
            data['status']="ok"
            data['message']=MESSAGE.POST_SUCCESS
            data['postid']=topicid
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
                offset=int(page*20)
                limit=20
                #query="select api_forumpost.id as id,api_forumpost.uid,username,topic,api_forumpost.body,api_forumpost.comments as comments,api_forumpost.likes as likes,api_forumpost.createdate as postdate from api_user,api_forumpost,api_forumtopic where api_user.id=api_forumpost.uid and api_forumpost.topicid=api_forumtopic.id and  api_forumtopic.id="+topicid
                #forumpost=ForumPost.objects.raw(query)
                #message=Message.objects(topicid=topicid)
                print "Fetching message"
                #message=Message.objects(topicid=topicid).fields(slice__comments=[offset, limit]).get()
                message = Comment.objects(topicid=topicid).skip(offset).limit(limit).order_by('-commentdate')
                print message
                postdata=messagesToJson(message)
                data={}
                data['posts']=postdata
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
