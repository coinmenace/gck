from imports import *




#list
#@csrf_protect
@csrf_exempt
def sync(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            data={}
            try:
                uid=request.POST.get("uid")
                purchaseid=request.POST.get("purchaseids")
                purchaseids=[]
                if purchaseid!=None:
                    purchaseids = purchaseid.split(",")
                if int(request.session.get("uid"))!=int(uid):
                    data={}
                    data['status']="failed"
                    data['message']=MESSAGE.INVALID_USERID
                    return JsonResponse(data)
                query="SELECT a.id as id,a.createdate as purchasedate,pid,comment,amount,tax,commission,voucher_code,status,a.uid as uid,description,b.thumbid as thumbid,b.name as product,catid,e.name as author,price,adddate,contentid,image_32X32,image_64X64,image_128X128,image_256X256,image_512X512,image_1024X1024,d.identifier as identifier,image_2048X2048,url,size,defaultkey,uploaddate,filename,duration,rdturl from api_purchases a,api_product b,api_thumbs c,api_content d,api_author e  where b.authorid=e.id and a.pid=b.id and c.id=b.thumbid and d.identifier=b.contentid and a.uid="+uid+" group by a.pid"
                purchases=Purchases.objects.raw(query)
                try:
                    print "Purchase data"
                    purchasedata = getPurchaseSync(siteurl,purchases,purchaseids)
                    print purchasedata
                    data = {}
                    data['products'] = purchasedata
                    data['status'] = "ok"
                    data['message'] = "successfully synced purchases"
                except Exception as ex:
                    print ex
                    data={}
                    data['status']="ok"
                    data['message']="Invalid purchase"
            except Exception as ex:
                print ex
                data={}
                data['status']="failed"
                data['message']="unable to sync purchases"
            return JsonResponse(data)
        else:
            data={}
            data['status']="failed"
            data['message']="invalid request.POST required"
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']="invalid session"
        return JsonResponse(data)