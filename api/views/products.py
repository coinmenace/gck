from imports import *


#list
#@csrf_protect
@csrf_exempt
def searchproducts(request):
    if request.session.get('isloggedin', True):
        if request.method == "GET":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                search_q=request.GET['q']
                #limit=request.GET['limit']
                #pager="LIMIT "+offset+","+limit
                if "page" in request.GET:
                    page=request.GET['page']
                else:
                    page=0
                offset=str(page*20)
                limit="20"
                pager="LIMIT "+offset+","+limit
                query="SELECT image_256X256 as image,image_512X512 as image2,image_1024X1024 as image3,product.id as id,category,author,product,description,price,size,readbyid,adddate from (SELECT  size,api_product.id as id,api_category.name as category,api_author.name as author,api_product.name as product,description,price,api_product.thumbid as thumbid,readbyid,adddate from api_product,api_category,api_author,api_content  WHERE  api_content.identifier=api_product.contentid AND api_product.authorid=api_author.id AND api_product.catid=api_category.id AND (api_product.name LIKE '%%"+search_q+"%%' OR api_product.description LIKE '%%"+search_q+"%%')) as product left join api_thumbs as thumbs on product.thumbid=thumbs.id  "+pager
                print query
                media=Product.objects.raw(query)
               #print media
                #media=Product.objects.raw("SELECT image_256X256 as image,image_512X512 as image2,image_1024X1024 as image3,product.id as id,category,author,product,description,price,size from (SELECT  size,api_product.id as id,api_category.name as category,api_author.name as author,api_product.name as product,description,price,api_product.thumbid as thumbid from api_product,api_category,api_author  WHERE api_product.authorid=api_author.id AND api_product.catid=api_category.id) as product left join api_thumbs as thumbs on product.thumbid=thumbs.id")
                productlist=productToJsonMobile(siteurl,media)
                data={}
                data['total']=Product.objects.count()
                data['products']=productlist
                data['status']="ok"
                data['message']=MESSAGE.PRODUCT_SUCCESS
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']=MESSAGE.PRODUCT_FAIL
            return JsonResponse(data)
        else:
            data={}
            data['status']="failed"
            data['message']=MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']=MESSAGE.INVALID_SESSION
        return JsonResponse(data)

#list
#@csrf_protect
@csrf_exempt
def listproducts(request,catid,page):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                if not catid:
                   catid=str(request.GET.get("catid"))
                else:
                    catid=str(catid)
                if not page:
                    page=int(request.GET.get("page"))
                else:
                    page=int(page)
                offset=str(page*20)
                limit="20"
                pager="LIMIT "+offset+","+limit
                query="SELECT image_256X256 as image,image_512X512 as image2,image_1024X1024 as image3,product.id as id,category,author,product,description,price,size,readbyid,adddate from (SELECT  size,api_product.id as id,api_category.name as category,api_author.name as author,api_product.name as product,description,price,api_product.thumbid as thumbid,readbyid,adddate from api_product,api_category,api_author,api_content  WHERE  api_product.catid='"+catid+"' AND api_content.identifier=api_product.contentid AND api_product.authorid=api_author.id AND api_product.catid=api_category.id) as product left join api_thumbs as thumbs on product.thumbid=thumbs.id "+pager
                print query
                media=Product.objects.raw(query)
                #media=Product.objects.raw("SELECT image_256X256 as image,image_512X512 as image2,image_1024X1024 as image3,product.id as id,category,author,product,description,price,size from (SELECT  size,api_product.id as id,api_category.name as category,api_author.name as author,api_product.name as product,description,price,api_product.thumbid as thumbid from api_product,api_category,api_author  WHERE api_product.authorid=api_author.id AND api_product.catid=api_category.id) as product left join api_thumbs as thumbs on product.thumbid=thumbs.id")
                productlist=productToJsonMobile(siteurl,media)
                data={}
                data['total']=Product.objects.count()
                data['products']=productlist
                data['status']="ok"
                data['total']=Product.objects.count()
                data['message']=MESSAGE.PRODUCT_SUCCESS
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']=MESSAGE.PRODUCT_FAIL
            return JsonResponse(data)
        else:
            data={}
            data['status']="failed"
            data['message']=MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']=MESSAGE.INVALID_SESSION
        return JsonResponse(data)


#list
#@csrf_protect
@csrf_exempt
def listproductswithid(request,productid):
    if request.session.get('isloggedin', False):
        if request.method == "GET":

            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                if not productid:
                    productid=str(request.GET.get("page"))
                else:
                    productid=str(productid)
                media=Product.objects.raw("SELECT image_256X256 as image,image_512X512 as image2,image_1024X1024 as image3,product.id as id,category,author,product,description,price from (SELECT  api_product.id as id,api_category.name as category,api_author.name as author,api_product.name as product,description,price,api_product.thumbid as thumbid from api_product,api_category,api_author  WHERE api_product.id="+productid+" AND api_product.authorid=api_author.id AND api_product.catid=api_category.id) as product left join api_thumbs as thumbs on product.thumbid=thumbs.id ")
                productlist=productToJsonMobile(siteurl,media)
                data={}
                data['total']=Product.objects.count()
                data['products']=productlist
                data['status']="ok"
                data['message']=MESSAGE.PRODUCT_SUCCESS
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']=MESSAGE.PRODUCT_FAIL
            return JsonResponse(data)
        else:
            data={}
            data['status']="failed"
            data['message']=MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']=MESSAGE.INVALID_SESSION
        return JsonResponse(data)

# @csrf_protect
@csrf_exempt
def listrelatedproducts(request, catid):
    if request.session.get('isloggedin', False):
        if request.method == "GET":

            response = verifySignature(request)
            if response['status'] == "failed":
                return JsonResponse(response)
            try:
                if not catid:
                    catid = str(request.GET.get("catid"))
                else:
                    catid = str(catid)
                query="SELECT image_256X256 as image,image_512X512 as image2,image_1024X1024 as image3,product.id as id,category,author,product,description,price from (SELECT  api_product.id as id,api_category.name as category,api_author.name as author,api_product.name as product,description,price,api_product.thumbid as thumbid from api_product,api_category,api_author  WHERE  api_product.authorid=api_author.id AND api_product.catid=api_category.id AND api_product.catid="+catid+") as product left join api_thumbs as thumbs on product.thumbid=thumbs.id LIMIT 4"
                print query
                p = Product.objects.raw(query)
                productlist = productToJsonMobile(siteurl, p)
                data = {}
                data['total'] = Product.objects.count()
                data['products'] = productlist
                data['status'] = "ok"
                data['message'] = MESSAGE.PRODUCT_SUCCESS
            except Exception as ex:
                print ex
                data = {}
                data['status'] = "failed"
                data['message'] = MESSAGE.PRODUCT_FAIL
            return JsonResponse(data)
        else:
            data = {}
            data['status'] = "failed"
            data['message'] = MESSAGE.INVALID_REQUEST_GET
            return JsonResponse(data)
    else:
        data = {}
        data['status'] = "failed"
        data['message'] = MESSAGE.INVALID_SESSION
        return JsonResponse(data)



#@csrf_protect
@csrf_exempt
def productcomment(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        productid=request.POST.get("pid")
        uid=request.POST.get("uid")
        message=request.POST.get("message")
        post=ProductComment.objects.create(uid=uid,body=message,productid=productid,isactive=1,createdate=timezone.now())
        data={}
        if post.id!=None:
            data['status']="ok"
            data['message']=MESSAGE.POST_SUCCESS
            data['postid']=post.id
        else:
            data['status']="failed"
            data['message']=MESSAGE.POST_FAILED


        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        return JsonResponse(data)


@csrf_exempt
def listproductcomment(request,pid,page):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            print "List Forums"
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                if not page:
                    page=int(request.GET.get("page"))
                else:
                    page=int(page)
                if not pid:
                    pid=str(request.GET.get("pid"))
                else:
                    pid=str(pid)
                offset=str(page*20)
                limit="20"
                pager="LIMIT "+offset+","+limit
                query="select a.id as id,username,c.name,body,a.createdate as postdate from api_productcomment a,api_user b,api_product c where a.uid=b.id and a.productid=c.id and  a.productid="+pid
                print query
                productpost=ProductComment.objects.raw(query)
                forumlist=productpostToJsonMobile(productpost)
                data={}
                data['topics']=forumlist
                data['status']="ok"
                data['message']="successfully listed product comments"
                #print data
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']="unable to list product comments"
            return JsonResponse(data)
        else:
            data={}
            data['status']="failed"
            data['message']="invalid request.GET required"
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']="invalid session id"
        return JsonResponse(data)


@csrf_protect
@csrf_exempt
def likeproduct(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        pid=request.POST.get("pid")
        uid=request.POST.get("uid")
        print pid,uid
        product=None
        try:
            product=ProductStats.objects.get(pid=pid,uid=uid)
        except Exception as ex:
            print ex
        if product==None:
            post=ProductStats.objects.create(pid=pid,uid=uid,like=1)
        else:
            print product
            product.like=1
            product.save()
        data={}
        if product.id!=None:
            data['status']="ok"
            data['message']=MESSAGE.SUCCESS
            data['productid']=product.id
        else:
            data['status']="failed"
            data['message']=MESSAGE.FAILED


        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        return JsonResponse(data)

@csrf_protect
@csrf_exempt
def unlikeproduct(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        pid=request.POST.get("pid")
        uid=request.POST.get("uid")
        product=None
        try:
            product=ProductStats.objects.get(pid=pid,uid=uid)
        except Exception as ex:
            print ex
        data={}
        if product!=None:
            product.like=0
            product.save()
            data['status']="ok"
            data['message']=MESSAGE.SUCCESS
            data['productid']=product.id
        else:
            data['status']="failed"
            data['message']=MESSAGE.FAILED
        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        return JsonResponse(data)


@csrf_protect
@csrf_exempt
def rateproduct(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        pid=request.POST.get("pid")
        uid=request.POST.get("uid")
        rating=request.POST.get("rating")
        product=None
        try:
            product=ProductStats.objects.get(pid=pid,uid=uid)
        except Exception as ex:
            print ex
        if product==None:
            product=ProductStats.objects.create(pid=pid,uid=uid,rating=rating)
        else:
            product.rating=rating
            product.save()
        data={}
        if product.id!=None:
            data['status']="ok"
            data['message']=MESSAGE.SUCCESS
            data['productid']=product.id
        else:
            data['status']="failed"
            data['message']=MESSAGE.FAILED


        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        return JsonResponse(data)

@csrf_protect
@csrf_exempt
def updatelistens(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        pid=request.POST.get("pid")
        uid=request.POST.get("uid")
        product=None
        try:
            product=ProductStats.objects.get(pid=pid,uid=uid)
        except Exception as ex:
            print ex
        if product==None:
            product=ProductStats.objects.create(pid=pid,uid=uid,listen=1)
        else:
            product.listen=product.listen+1
            product.save()
        data={}
        if product.id!=None:
            data['status']="ok"
            data['message']=MESSAGE.SUCCESS
            data['productid']=product.id
        else:
            data['status']="failed"
            data['message']=MESSAGE.FAILED


        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        return JsonResponse(data)


@csrf_protect
@csrf_exempt
def updatedownloads(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        pid=request.POST.get("pid")
        uid=request.POST.get("uid")
        product=None
        try:
            product=ProductStats.objects.get(pid=pid,uid=uid)
        except Exception as ex:
            print ex
        if product==None:
            product=ProductStats.objects.create(pid=pid,uid=uid,download=1)
        else:
            product.download=product.download+1
            product.save()
        data={}
        if product.id!=None:
            data['status']="ok"
            data['message']=MESSAGE.SUCCESS
            data['productid']=product.id
        else:
            data['status']="failed"
            data['message']=MESSAGE.FAILED


        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        return JsonResponse(data)



@csrf_exempt
def getdocument(request,pid=None):
    if request.method == "POST":
        print "Fetching samples"
        uid = request.POST.get("uid")
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        if pid==None:
            pid=request.POST.get("pid")
        product=None
        data = {}
        try:
            query="SELECT api_product.id as id,name,documenturl from api_product,api_content where api_product.contentid=api_content.identifier AND api_product.id="+str(pid)
            print query
            product=Product.objects.raw(query)
            data['status'] = "ok"
            data['message'] = MESSAGE.SUCCESS
            data['data']=documentToJson(siteurl,product)
        except Exception as ex:
            print ex
            data['status'] = "failed"
            data['message'] = "unable to download document"
        return JsonResponse(data)
    else:
        data={}
        data['message']="invalid method.POST required"
        data['status']="failed"
        return JsonResponse(data)



@csrf_exempt
def getsample(request,pid=None):
    if request.method == "GET":
        print "Fetching samples"
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        if pid==None:
            pid=request.POST.get("pid")
        product=None
        data = {}
        try:
            query="SELECT api_product.id as id,name,sampleurl from api_product,api_content where api_product.contentid=api_content.identifier AND api_product.id="+str(pid)
            print query
            product=Product.objects.raw(query)
            data['status'] = "ok"
            data['message'] = MESSAGE.SUCCESS
            data['data']=sampleToJson(siteurl,product)
        except Exception as ex:
            print ex
            data['status'] = "failed"
            data['message'] = "unable to download sample"
        return JsonResponse(data)
    else:
        data={}
        data['message']="invalid method.GET required"
        data['status']="failed"
        return JsonResponse(data)