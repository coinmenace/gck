from imports import *


def promo(request):
    if request.session.get('isloggedin', False):
        data['view']="promo"
        data['products'] = Product.objects.all()
        template = loader.get_template('manager_promo.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def createpromo(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            print request.POST
            productid=request.POST.get("productid")
            promocode=request.POST.get("promocode")
            startdate=request.POST.get("startdate")
            enddate = request.POST.get("enddate")
            description=request.POST.get("description")
            amount=request.POST.get("amount")
            isactive = 1
            promo=processPromo(productid,amount,promocode,description,isactive,startdate,enddate)
            if promo.id!=None:
                data={}
                data['status']="ok"
                data['message']="product added successfully"
            else:
                data={}
                data['message']="unable to add product"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("/manager/promo")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/promo")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def updatepromo(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            promoid = request.POST.get("promoid")
            productid=request.POST.get("productid")
            promocode=request.POST.get("promocode")
            startdate=request.POST.get("startdate")
            enable = request.POST.get("enable")
            print request.POST
            isactive = 0
            if enable=="on":
                isactive = 1
            enddate = request.POST.get("enddate")
            description=request.POST.get("description")
            amount=request.POST.get("amount")

            promo=processPromo(productid,amount,promocode,description,isactive,startdate,enddate,promoid)
            if promo.id!=None:
                data={}
                data['status']="ok"
                data['message']="product added successfully"
            else:
                data={}
                data['message']="unable to add product"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("/manager/promo")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/promo")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")

def listpromo(request):
    if request.session.get('isloggedin', False):
        data={}
        if "page" in request.GET:
            page = request.GET['page']
        else:
            page = 0
        offset = str(page * 20)
        limit = "20"
        pager = "LIMIT " + offset + "," + limit
        media=Promo.objects.raw("SELECT  api_promo.promocode as promocode,startdate,enddate,api_promo.id as id,api_product.name as product,api_product.description as productdescription,api_promo.description as promodescription,price,api_product.thumbid as thumbid,api_promo.amount as promoprice,api_thumbs.image_256X256 as image,api_promo.isactive as status,api_promo.createdate as createdate from api_product,api_promo,api_thumbs  WHERE api_product.id=api_promo.productid and api_thumbs.id=api_product.thumbid "+pager)
        data={}
        data['total']= Promo.objects.count()
        data['rows']=promoToJsonMobile(media)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deletepromo(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            promoid=request.GET['id']
        else:
            promoid=id
        promo=Promo.objects.get(id=promoid)
        promo.delete()
        return HttpResponseRedirect("/manager/content")
    else:
        return HttpResponseRedirect("login")


def processPromo(productid,amount,promocode,description,isactive,startdate,enddate,promoid=None):
    if promoid == None:
        promo = Promo.objects.create(productid=productid, amount=amount, promocode=promocode, description=description,
                                     isactive=isactive, startdate=startdate, enddate=enddate, createdate=timezone.now())
    else:
        promo = Promo.objects.get(id=promoid)
        promo.productid = productid
        promo.amount = amount
        promo.promocode = promocode
        promo.description = description,
        promo.isactive = isactive
        promo.startdate = startdate
        promo.enddate = enddate
        promo.save()

    return promo