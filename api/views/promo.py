from imports import *

#list
#@csrf_protect
@csrf_exempt
def getpromo(request):
    if request.session.get('isloggedin', False):
        data={}
        query = "SELECT  api_promo.promocode as promocode,startdate,enddate,api_promo.id as id,api_product.name as product,api_product.description as productdescription,api_promo.description as promodescription,price,api_product.thumbid as thumbid,api_promo.amount as promoprice,api_thumbs.image_256X256 as image from api_product,api_promo,api_thumbs  WHERE api_product.id=api_promo.productid and api_thumbs.id=api_product.thumbid"
        print query
        media = Promo.objects.raw(query)
        data={}
        try:
            data['status'] = "ok"
            data['message'] = "sucessfully listed promotions"
            data['total']= Promo.objects.count()
            data['data']= promoToJsonMobile(media)
        except Exception as ex:
            data = {}
            data['status'] = "failed"
            data['message'] = "unable to list promotions"
        return JsonResponse(data)
    else:
        data = {}
        data['status'] = "failed"
        data['message'] = "unable to list promotions"
        return JsonResponse(data)