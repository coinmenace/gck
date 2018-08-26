from channels import Group
from imports import *


def notification(request):
    message=request.GET['message']
    result = {}
    result['message'] = message
    result['status']="ok"
    Group('broadcast').send({
        'text': json.dumps(result)
    })
    response={}
    response['status']="ok"
    return JsonResponse(response)