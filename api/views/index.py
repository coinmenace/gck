from imports import *

@csrf_exempt
@ensure_csrf_cookie
def index(request):
    if request.method == "GET":
        if "HTTP_X_AP_SIGNATURE" not in request.META:
            data['message']="invalid signature"
        if "HTTP_X_NL_API_VERSION" not in request.META:
            data['message']="unknown api version"
        if "HTTP_VERSION" not in request.META:
            data['message']="unknown app version"
        if "HTTP_X_NL_KEY" not in request.META:
            data['message']="invalid key"
        return JsonResponse(data)
    else:
        return JsonResponse(data)
