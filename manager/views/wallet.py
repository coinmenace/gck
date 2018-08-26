from imports import *


def wallet(request):
    if request.session.get('isloggedin', False):
        data['username']=request.session.get("username")
        data['view']="wallet"
        if "creditwallet" in data:
            del data['creditwallet']
        if "debitwallet" in data:
            del data['debitwallet']
        template = loader.get_template('manager_wallet.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def viewcreditwallet(request,id):
    if request.session.get('isloggedin', False):
        data['view']="users"
        user=User.objects.get(id=id)
        data['user']=user
        data['creditwallet']=True
        template = loader.get_template('manager_wallet.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def viewdebitwallet(request,id):
    if request.session.get('isloggedin', False):
        data['view']="users"
        user=User.objects.get(id=id)
        data['user']=user
        data['debitwallet']=True
        template = loader.get_template('manager_wallet.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def creditwallet(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            uid=request.POST.get("uid")
            username=request.POST.get("username")
            amount=request.POST.get("amount")
            if settings.maxamount > amountval:
                request.session['message'] = "unable to credit account. amount is too large"
                request.session['status'] = "failed"
                return HttpResponseRedirect("/manager/wallet")
            wallet=Wallet.objects.get(uid=uid)
            oldbalance=wallet.balance
            wallet.balance=float(oldbalance)+float(amount)
            wallet.save()
            tax=0.0
            commission=0.0
            description="Credit wallet of %s with sum %f by admin (Previous balance:%f)" % (username,float(amount),float(oldbalance),)
            Transactions.objects.create(uid=uid,amount=amount,description=description,tax=tax,commission=commission,status=1,createdate=timezone.now())
            return HttpResponseRedirect("/manager/wallet")
        else:
            data={}
            request.session['message']="user with this username exists"
            request.session['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/wallet")

    else:
        data={}
        context = {
        'data': data
        }
        return HttpResponseRedirect("../login")



def debitwallet(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            uid=request.POST.get("uid")
            username=request.POST.get("username")
            amount=request.POST.get("amount")
            amountval = int(amount)
            if settings.maxamount > amountval:
                request.session['message'] = "unable to debit account. amount is too large"
                request.session['status'] = "failed"
                return HttpResponseRedirect("/manager/wallet")
            wallet=Wallet.objects.get(uid=uid)
            oldbalance=wallet.balance
            newbalance=float(oldbalance)-float(amount)
            if newbalance>0:
                wallet.balance=newbalance
                wallet.save()
                tax=0.0
                commission=0.0
                description="Debit wallet of %s with sum %f by admin(Previous balance:%f)"%(username,float(amount),float(oldbalance),)
                Transactions.objects.create(uid=uid,amount=amount,description=description,tax=tax,commission=commission,status=1,createdate=timezone.now())
                request.session['message']="account debited successfully"
                request.session['status']="ok"
            else:
                request.session['message']="unable to debit account."
                request.session['status']="failed"
            return HttpResponseRedirect("/manager/wallet")
        else:
            data={}
            request.session['message']="user with this username exists"
            request.session['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("/manager/wallet")

    else:
        data={}
        context = {
        'data': data
        }
        return HttpResponseRedirect("../login")




def deletewallet(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            walletid=request.GET['id']
        else:
            walletid=id
        wallet=Wallet.objects.get(id=walletid)
        wallet.delete()
        return HttpResponseRedirect("/manager/wallet")
    else:
        return HttpResponseRedirect("login")


def listwallet(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        wallets=Wallet.objects.raw("SELECT  a.id as id,a.username as username,b.balance,b.createdate as createdate from api_user a,api_wallet b WHERE a.id=b.uid "+pager)
        data={}
        data['total']= Wallet.objects.count()
        data['rows']=walletToJson(wallets)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")