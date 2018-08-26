from imports import *


#list
#@csrf_protect
@csrf_exempt
def searchusers(request):
    if request.session.get('isloggedin', True):
        if request.method == "GET":
            #response=verifySignature(request)
            #if response['status']=="failed":
            #    return JsonResponse(response)
            print "user search"
            try:
                search_q=request.GET['q']
                if "page" in request.GET:
                    page=request.GET['page']
                else:
                    page=0
                offset=str(page*20)
                limit="20"
                uid= request.session.get("uid")
                pager="LIMIT "+offset+","+limit
                query="SELECT a.id as id,b.firstname,b.lastname,b.profilepics,a.username from api_user a,api_profile b WHERE a.id=b.uid AND a.username LIKE '%%"+search_q+"%%' OR b.firstname  LIKE '%%"+search_q+"%%' OR b.lastname  LIKE '%%"+search_q+"%%' "+pager
                print query
                users=User.objects.raw(query)
                userlist=userToJsonMobile2(uid,users)
                data={}
                data['total']=len(userlist)
                data['users']=userlist
                data['status']="ok"
                data['message']="successfully searched users"
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']="unable to search users"
            return JsonResponse(data)
        else:
            data={}
            data['status']="failed"
            data['message']="invalid request.required GET"
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']="invalid request.invalid session"
        return JsonResponse(data)