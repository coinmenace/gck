from imports import *


def index(request):
    if request.session.get('isloggedin', False):
        data['authors']=Author.objects.count()
        data['users']=User.objects.count()
        data['content']=Product.objects.count()
        data['purchases']=Purchases.objects.count()
        data['username']=request.session.get("username")
        data['orders'] = Purchases.objects.count()
        data['sales'] = Purchases.objects.filter(status=1).count()
        data['items'] = Product.objects.count()
        data['customers'] = User.objects.count()
        query="select id,name,count(name) as percent from api_device group by name"
        data['devices']=Device.objects.raw(query)
        template = loader.get_template('manager_dashboard.html')
        data['view']="dashboard"
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")