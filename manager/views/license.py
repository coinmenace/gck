from imports import *

def license(request):
    if request.session.get('isloggedin', False):
        data['view']="license"
        data['username']=request.session.get("username")
        template = loader.get_template('manager_license.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def listlicenses(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        license=License.objects.raw("SELECT  api_license.id as id,lkey as licensekey,username,api_product.name as product,licensedate  from api_license,api_user,api_product where api_user.id=api_license.uid and api_license.pid=api_product.id "+pager)
        data={}
        data['total']=  License.objects.count()
        data['rows']=licensesToJson(license)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deletelicenses(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            licenseid=request.GET['id']
        else:
            licenseid=id
        license=License.objects.get(id=licenseid)
        license.delete()
        return HttpResponseRedirect("../../license")
    else:
        return HttpResponseRedirect("login")