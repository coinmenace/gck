from imports import *

#verify account
#@csrf_protect
@csrf_exempt
def verify(request):
    if request.session.get('isloggedin', False):

        return JsonResponse(data)
    else:
        return JsonResponse(data)