from imports import *

def transactions(request):
    if request.session.get('isloggedin', False):
        data['view']="transactions"
        data['username']=request.session.get("username")
        template = loader.get_template('manager_transactions.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def listtransactions(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        purchases=Purchases.objects.raw("select api_purchases.id as id,api_product.name as productname,api_purchases.amount as price,api_user.username as username,api_purchases.createdate as purchasedate,commission,voucher_code,api_purchases.status as status from api_purchases,api_product,api_user where api_purchases.pid=api_product.id and api_user.id=api_purchases.uid "+pager)
        for p in purchases:
            print p.username
        data={}
        data['total']=  Purchases.objects.count()
        data['rows']=PurchasesToJson(purchases)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")
