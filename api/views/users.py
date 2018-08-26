from imports import *


def searchuser(request):
    if request.session.get('isloggedin', True):
        if request.method == "GET":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                search_q=request.GET['q']
                #limit=request.GET['limit']
                #pager="LIMIT "+offset+","+limit
                if "page" in request.GET:
                    page=request.GET['page']
                else:
                    page=0
                offset=str(page*20)
                limit="20"
                pager="LIMIT "+offset+","+limit
                query="SELECT username,uid,profilepic,firstname,lastname from api_user a,api_profile b WHERE a.id=b.uid and (b.firstname like '%"+search_q+"%' OR b.lastname like '%"+search_q+"%' OR a.username like '%"+search_q+"%' ) "+pager
                user=User.objects.raw(query)
                userlist=userToJsonMobile(siteurl,user)
                data={}
                data['total']=Product.objects.count()
                data['users']=userlist
                data['status']="ok"
                data['message']="sucessfully listed users"
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']="unable to fetch users"
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
