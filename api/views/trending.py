from imports import *

#list
#@csrf_protect
@csrf_exempt
def listtrending(request):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                query="SELECT image_256X256 as image,image_512X512 as image2,image_1024X1024 as image3,product.id as id,category,author,product,description,price,size from (SELECT  size,api_product.id as id,api_category.name as category,api_author.name as author,api_product.name as product,description,price,api_product.thumbid as thumbid from api_product,api_category,api_author,api_content  WHERE  api_content.identifier=api_product.contentid AND api_product.authorid=api_author.id AND api_product.catid=api_category.id) as product left join api_thumbs as thumbs on product.thumbid=thumbs.id LIMIT 0,20"
                #print query
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

