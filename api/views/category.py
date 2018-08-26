from imports import *



#list categories
#@csrf_protect
@csrf_exempt
def listcategories(request):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                categories=Category.objects.all()
                categorylist=getCategoryDict(categories)
                data={}
                data['categories']=categorylist
                data['status']="ok"
                data['message']=MESSAGE.CATEGORY_SUCCESS
            except Exception as ex:
                data={}
                data['status']="failed"
                data['message']=MESSAGE.CATEGORY_FAIL
            return JsonResponse(data)
        else:
            data['status']="failed"
            data['message']=MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']=MESSAGE.INVALID_SESSION
        return JsonResponse(data)
