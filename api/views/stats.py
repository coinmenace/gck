from imports import  *

#register device
#@csrf_protect
@csrf_exempt
def stats(request):
    if request.session.get('isloggedin', False):

        return JsonResponse(data)
    else:
        return JsonResponse(data)