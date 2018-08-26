from imports import *


#list authors
#@csrf_protect
@csrf_exempt
def listauthors(request):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            print "List Authors"
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                authors=Author.objects.raw("SELECT  api_author.id as id,image_256X256 as image,name,joindate from api_author  left join api_thumbs on  api_author.thumbid =api_thumbs.id")
                authorlist=authorsToJsonMobile(siteurl,authors)
                data={}
                data['authors']=authorlist
                data['status']="ok"
                data['message']=MESSAGE.AUTHOR_SUCCESS
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']=MESSAGE.AUTHOR_FAIL
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