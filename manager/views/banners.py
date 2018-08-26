from imports import *


def banner(request):
    if request.session.get('isloggedin', False):
        data['view']="banner"
        data['username']=request.session.get("username")
        data['categories']=Category.objects.all()
        data['authors']=Author.objects.all()
        template = loader.get_template('manager_banners.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def createbanner(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            catid=request.POST.get("catid")
            authorid=request.POST.get("authorid")
            description=request.POST.get("description")
            fulltext = request.POST.get("fulltext")
            price=request.POST.get("price")
            sample = request.POST.get("sample")
            generatesample=0
            duration=0
            if sample=="on":
                generatesample=1
                duration = int(request.POST.get("duration"))
            try:
                poster=request.FILES["banner"]
                thumbid=generatethumbs(poster)
            except:
                thumbid=0
            file=request.FILES["media"]
            filename=file.name
            data=file.read()
            contentid=str(uuid.uuid4())

            #fullname="website/static/media/samples/"+filename
            #fullname="website/static/media/live/"+filename
            secret=randomgen(16)
            generatemediadir(generatesample,duration,secret,contentid,filename,data)
            textid=0
            if len(fulltext)>10:
                contenttext=ContentText.objects.create(fulltext=fulltext)
                textid=contenttext.id

            product=Product.objects.create(name=name,thumbid=thumbid,hassample=generatesample,contentid=contentid,catid=catid,authorid=authorid,description=description,textid=textid,price=price,adddate=timezone.now())
            if product.id!=None:
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
            return HttpResponseRedirect("../content")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../content")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")

def updatebanner(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            catid=request.POST.get("catid")
            authorid=request.POST.get("authorid")
            description=request.POST.get("description")
            fulltext = request.POST.get("fulltext")
            price=request.POST.get("price")
            sample = request.POST.get("sample")
            generatesample=0
            duration=0
            if sample=="on":
                generatesample=1
                duration = int(request.POST.get("duration"))
            try:
                poster=request.FILES["poster"]
                thumbid=generatethumbs(poster)
            except:
                thumbid=0
            file=request.FILES["media"]
            filename=file.name
            data=file.read()
            contentid=str(uuid.uuid4())

            #fullname="website/static/media/samples/"+filename
            #fullname="website/static/media/live/"+filename
            secret=randomgen(16)
            generatemediadir(generatesample,duration,secret,contentid,filename,data)
            textid=0
            if len(fulltext)>10:
                contenttext=ContentText.objects.create(fulltext=fulltext)
                textid=contenttext.id

            product=Product.objects.create(name=name,thumbid=thumbid,hassample=generatesample,contentid=contentid,catid=catid,authorid=authorid,description=description,textid=textid,price=price,adddate=timezone.now())
            if product.id!=None:
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
            return HttpResponseRedirect("../content")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../content")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")

def listbanner(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        media=Product.objects.raw("SELECT image_256X256 as image,product.id as id,category,author,product,description,price from (SELECT  api_product.id as id,api_category.name as category,api_author.name as author,api_product.name as product,description,price,api_product.thumbid as thumbid from api_product,api_category,api_author  WHERE api_product.authorid=api_author.id AND api_product.catid=api_category.id) as product left join api_thumbs as thumbs on product.thumbid=thumbs.id "+pager)
        data={}
        data['total']= Product.objects.count()
        data['rows']=productToJson(media)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deletebanner(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            mediaid=request.GET['id']
        else:
            mediaid=id
        product=Product.objects.get(id=mediaid)
        product.delete()
        return HttpResponseRedirect("../../content")
    else:
        return HttpResponseRedirect("login")