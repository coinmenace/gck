# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader
from django.db.models import *
from api.models import *
import time
import csv
from django.utils import timezone
from django.utils.encoding import *
import hashlib
from celery.result import AsyncResult
from celery.task.control import *
from celery import task, current_task,current_app
import os
import codecs
from celery import Celery
from django.conf import settings
from anyjson import serialize
import uuid
from os import listdir
from os.path import isfile, join
from django import template
import random, string
import uuid
from task import *
from aesutil import *
# Create your views here.
import settings
import messages as MESSAGE
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
# Create your views here.
siteurl=settings.siteurl
data={"sitename":"audio Learn"}
def index(request):
    if request.session.get('isloggedin', False):
        data['authors']=Author.objects.count()
        data['users']=User.objects.count()
        data['content']=Product.objects.count()
        data['purchases']=Purchases.objects.count()
        data['username']=request.session.get("username")
        template = loader.get_template('manager_dashboard.html')
        data['view']="dashboard"
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def pushmessage(request):
    redis_publisher = RedisPublisher(facility='subscribe', users=[request.GET.get('user')])
    #redis_publisher = RedisPublisher(facility='subscribe', broadcast=True)
    data={}
    data['message']="You got it"
    data['audio']=""
    messagebody="""
    {
   "alert": "Updates Available",
   "badge": 1,
   "data": "{'version':'1.13','size':'14MB'}",
   "priority": "high",
   "sound": "DefaultNotificationSound",
   "gcmNotification": {
     "title": "The Title For The App",
     "icon": "TheIcon",
     "body": "The Notification Body",
     "sound": "OverrideSound",
     "color": "Blue",
     "tag": "TheTag",
     "collapseKey": "TheCollapseKey",
     "delayWhileIdle": true,
     "timeToLive": 10,
     "restrictedPackageName": "com.sap.test",
     "clickAction": "TheClickAction",
     "bodyLocKey": "message",
     "bodyLocArgs": "[\"msg1\",\"msg2\"]",
     "titleLocKey": "titleMessage",
     "titleLocArgs": "[\"tmsg1\",\"tmsg2\"]"
    },
   "customParameters": {
     "gcm.badge": 2
   }
 }
"""
    message = RedisMessage(messagebody)
    # and somewhere else
    redis_publisher.publish_message(message)
    return JsonResponse(data)


def login(request):
    template = loader.get_template('manager_login.html')
    data['view']="login"
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))
    

def users(request):
    if request.session.get('isloggedin', False):
        data['username']=request.session.get("username")
        data['view']="users"
        adminrole=AdminRole.objects.all()
        data['role']=adminrole
        template = loader.get_template('manager_users.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def authors(request):
    if request.session.get('isloggedin', False):
        print "Authors"
        data['view']="authors"
        data['username']=request.session.get("username")
        authors=Author.objects.all()
        data['authors']=authors
        template = loader.get_template('manager_authors.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def books(request):
    if request.session.get('isloggedin', False):
        data['view']="books"
        data['username']=request.session.get("username")
        data['collections']=Collection.objects.all()
        data['books']=Book.objects.all()
        data['authors']=Author.objects.all()
        template = loader.get_template('manager_books.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def content(request):
    if request.session.get('isloggedin', False):
        data['view']="content"
        data['username']=request.session.get("username")
        data['categories']=Category.objects.all()
        data['authors']=Author.objects.all()
        template = loader.get_template('manager_content.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def forums(request):
    if request.session.get('isloggedin', False):
        data['view']="forums"
        data['username']=request.session.get("username")
        data['forumtopic']=ForumTopic.objects.all()
        template = loader.get_template('manager_forum.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

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

def promo(request):
    if request.session.get('isloggedin', False):
        data['view']="promo"
        data['username']=request.session.get("username")
        authors=Author.objects.all()
        data['authors']=authors
        template = loader.get_template('manager_promo.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def messages(request):
    if request.session.get('isloggedin', False):
        data['view']="messages"
        data['username']=request.session.get("username")
        authors=Author.objects.all()
        data['authors']=authors
        template = loader.get_template('manager_messages.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def settings(request):
    if request.session.get('isloggedin', False):
        data['view']="settings"
        data['username']=request.session.get("username")
        authors=Author.objects.all()
        data['authors']=authors
        template = loader.get_template('manager_settings.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def logout(request):
    	for key in request.session.keys():
		del request.session[key]
	request.session.modified = True
	return HttpResponseRedirect("login")

def auth(request):
    if request.method == "POST":
            username=request.POST.get("username")
            passwd=request.POST.get("password")
            password=hashlib.sha256(passwd).hexdigest()
            try:
                admin=Admin.objects.filter(Q(username=username) & Q(password=password)).get()
                if admin.username!=None:
                    data={}
                    request.session['isloggedin']=True
                    request.session['username']=username
                    request.session['uid']=admin.id
                    request.session['role']=admin.role
                    return HttpResponseRedirect("/manager")
                
                else:
                    request.session['isloggedin']=False
                    return HttpResponseRedirect("login")
            except Exception as ex:
                print ex
                request.session['isloggedin']=False
                return HttpResponseRedirect("login")
                
            
            
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def listadmin(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        admin=Admin.objects.raw("SELECT  api_admin.id as id,api_adminrole.name as role,username,status from api_admin,api_adminrole WHERE api_admin.role=api_adminrole.id "+pager)
        data={}
        data['total']= Admin.objects.count()
        data['rows']=adminToJson(admin)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deleteadmin(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            adminid=request.GET['id']
        else:
            adminid=id
        admin=Admin.objects.get(id=adminid)
        admin.delete()
        return HttpResponseRedirect("../../users")
    else:
        return HttpResponseRedirect("login")

def listusers(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        users=User.objects.raw("SELECT  api_user.id as id,firstname,lastname,email,telephone,username,isphoneverified,isemailverified,status,api_user.createdate as createdate from api_user,api_profile WHERE api_user.id=api_profile.uid "+pager)
        data={}
        data['total']= User.objects.count()
        data['rows']=usersToJson(users)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deleteuser(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            userid=request.GET['id']
        else:
            userid=id
        user=User.objects.get(id=userid)
        user.delete()
        profile=Profile.objects.get(uid=userid)
        profile.delete()
        return HttpResponseRedirect("../../users")
    else:
        return HttpResponseRedirect("login")


def listmedia(request):
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

def deletemedia(request,id):
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


def listauthors(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        authors=Author.objects.raw("SELECT  api_author.id as id,image_256X256 as image,name,joindate from api_author  left join api_thumbs on  api_author.thumbid =api_thumbs.id "+pager)
        data={}
        data['total']=  Author.objects.count()
        data['rows']=authorsToJson(authors)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deleteauthors(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            authorid=request.GET['id']
        else:
            authorid=id
        author=Author.objects.get(id=authorid)
        author.delete()
        return HttpResponseRedirect("../../authors")
    else:
        return HttpResponseRedirect("login")

def listforums(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        forum=ForumTopic.objects.raw("SELECT  api_forumtopic.id as id,topic,comments,likes,isactive,api_forumtopic.createdate as createdate from api_forumtopic "+pager)
        data={}
        data['total']=  ForumTopic.objects.count()
        data['rows']=forumToJson(forum)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def deleteforums(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            forumid=request.GET['id']
        else:
            forumid=id
        forum=ForumTopic.objects.get(id=forumid)
        forum.delete()
        return HttpResponseRedirect("../../forums")
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


def createuser(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            username=request.POST.get("username")
            passwd=request.POST.get("password")
            secret=hashlib.md5(passwd).hexdigest()
            role=request.POST.get("role")
            print role
            print secret
            password=hashlib.sha256(passwd).hexdigest()
            verifyuser={}
            user={}
            user['id']=None
            verifyuser['username']=None
            try:
                userobject=Admin.objects.filter(Q(username=username)).get()
                verifyuser['username']=userobject.username
            except Exception as ex:
                print ex
            if verifyuser['username']==None:
                status=1
                user=Admin.objects.create(username=username,password=password,role=role,secret=secret,status=status,createdate=timezone.now())
                if user.id!=None:
                    uid=user.id
                    data={}
                    data['uid']=uid
                    data['username']=username
                    data['status']="ok"
                    data['message']="admin user created successfully"
                else:
                    data={}
                    data['message']="unable to create admin user"
                    data['status']="failed"
            else:
                data={}
                data['message']="admin user with this username exists"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../users")
        else:
            data={}
            data['message']="admin user with this username exists"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../users")
        
    else:
        data={}
        context = {
        'data': data
        }
        return HttpResponseRedirect("../login")



def createrole(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            role=AdminRole.objects.create(name=name,createdate=timezone.now())
            if role.id!=None:
                data={}
                data['status']="ok"
                data['message']="admin role created successfully"
            else:
                data={}
                data['message']="unable to create admin role"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../users")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../users")
        
    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")

def createauthor(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            uid=request.POST.get("uid")
            poster=request.FILES["picture"]
            filename=poster.name
            thumbid=generatethumbs(poster)
            role=Author.objects.create(name=name,thumbid=thumbid,joindate=timezone.now())
            if role.id!=None:
                data={}
                data['status']="ok"
                data['message']="category created successfully"
            else:
                data={}
                data['message']="unable to create category"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../authors")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../authors")
        
    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")

def createcollection(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            description=request.POST.get("description")
            collection=Collection.objects.create(name=name,description=description,createdate=timezone.now())
            if collection.id!=None:
                data={}
                data['status']="ok"
                data['message']="collection created successfully"
            else:
                data={}
                data['message']="unable to create collection"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../books")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../books")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def deletecollection(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            collectionid=request.GET['id']
        else:
            collectionid=id
        collection=Collection.objects.get(id=collectionid)
        collection.delete()
        return HttpResponseRedirect("../../books")
    else:
        return HttpResponseRedirect("login")



def listbook(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        media=Book.objects.raw("SELECT api_author.name as author,* from api_books,api_author WHERE api_book.authorid=api_author.id "+pager)
        data={}
        data['total']= Book.objects.count()
        data['rows']=booksToJson(media)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")


def createbook(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            description=request.POST.get("description")
            authorid=request.POST.get("authorid")
            isbn=request.POST.get("isbn")
            publishdate=request.POST.get("publishdate")

            book=Book.objects.create(name=name,description=description,authorid=authorid,isbn=isbn,publishdate=publishdate,createdate=timezone.now())
            if book.id!=None:
                data={}
                data['status']="ok"
                data['message']="book created successfully"
            else:
                data={}
                data['message']="unable to create book"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../books")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../books")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def deletebook(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            bookid=request.GET['id']
        else:
            bookid=id
        book=Book.objects.get(id=bookid)
        book.delete()
        return HttpResponseRedirect("../../books")
    else:
        return HttpResponseRedirect("login")


def createcategory(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            role=Category.objects.create(name=name,createdate=timezone.now())
            if role.id!=None:
                data={}
                data['status']="ok"
                data['message']="category created successfully"
            else:
                data={}
                data['message']="unable to create category"
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


def deletecategory(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            categoryid=request.GET['id']
        else:
            categoryid=id
        category=Category.objects.get(id=categoryid)
        category.delete()
        return HttpResponseRedirect("../../content")
    else:
        return HttpResponseRedirect("login")


def createforumtopic(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            topic=request.POST.get("topic")
            uid=request.session.get("uid")
            forumtopic=ForumTopic.objects.create(topic=topic,uid=uid,createdate=timezone.now())
            if forumtopic.id!=None:
                data={}
                data['status']="ok"
                data['message']="forumtopic created successfully"
            else:
                data={}
                data['message']="unable to create forumtopic"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../forums")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../forums")
        
    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")








#create book
def createbook(request):
    if request.session.get('ismanagerloggedin', False):
        data={}
        name=request.POST['name']
        description=request.POST['description']
        book=Book.objects.create(name=name,description=description)
        return HttpResponseRedirect("../book")
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")



#update book
def updatebook(request):
    if request.session.get('ismanagerloggedin', False):
        data={}
        id=request.POST["id"]
        name=request.POST["name"]
        description=request.POST["description"]
        authorid=request.POST["authorid"]
        isbn=request.POST["isbn"]
        publishdate=request.POST["publishdate"]
        createdate=request.POST["createdate"]
        book=Book.objects.update(name=name,description=description,authorid=authorid,isbn=isbn,publishdate=publishdate,createdate=createdate)
        data={}
        data['total']= Book.objects.count()
        data['rows']=booksToJson(book)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

#list book
def listbook(request):
    if request.session.get('isloggedin', False):
        if request.method == "GET":
            response=verifySignature(request)
            if response['status']=="failed":
                return JsonResponse(response)
            try:
                book=Book.objects.all()
                listdata=getBookDict(book)
                data={}
                data['book']=listdata
                data['status']="ok"
                data['message']=MESSAGE.BOOK_SUCCESS
            except Exception as ex:
                data={}
                data['status']="failed"
                data['message']=MESSAGE.BOOK_FAIL
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

#delete book
def deletebook(request):
    if request.session.get('ismanagerloggedin', False):
        data={}
        id=request.GET.get('id','')
        book=Book.objects.get(id=id)
        book.delete()
        return HttpResponseRedirect("../book")
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")







def uploadcontent(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            catid=request.POST.get("catid")
            authorid=request.POST.get("authorid")
            description=request.POST.get("description")
            price=request.POST.get("price")
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
            generatemediadir(secret,contentid,filename,data)
            product=Product.objects.create(name=name,thumbid=thumbid,contentid=contentid,catid=catid,authorid=authorid,description=description,price=price,adddate=timezone.now())
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

def generateauthordir():
    if not os.path.exists("static/"):
        os.mkdir("static")
    if not os.path.exists("static/authors"):
        os.mkdir("static/authors")
    if not os.path.exists("static/authors/thumb"):
        os.mkdir("static/authors/thumb")

def generatethumbs(poster):
    if not os.path.exists("website/static/thumbs"):
        os.mkdir("website/static/thumbs/")
    if not os.path.exists("website/static/thumbs/tmp"):
        os.mkdir("website/static/thumbs/tmp/")
    print poster.name
    data=poster.read()
    print "File size %d  ",len(data)
    with open("website/static/thumbs/tmp/"+poster.name,"w+") as f:
        f.write(data)
        f.close()
    result={}
    result['uploaddir']="website/static/thumbs/"
    result['fullname']="website/static/thumbs/tmp/"+poster.name
    result['file']=poster.name
    response=generateImageThumbNails.delay(result)
    identifier=response.id
    filename=poster.name.split(".")[0]
    image_32X32=identifier+"/"+filename+"_32_32.png"
    image_64X64=identifier+"/"+filename+"_64_64.png"
    image_128X128=identifier+"/"+filename+"_128_128.png"
    image_256X256=identifier+"/"+filename+"_256_256.png"
    image_512X512=identifier+"/"+filename+"_512_512.png"
    image_1024X1024=identifier+"/"+filename+"_1024_1024.png"
    image_2048X2048=identifier+"/"+filename+"_2048_2048.png"
    thumb=Thumbs.objects.create(image_32X32=image_32X32,image_64X64=image_64X64,image_128X128=image_128X128,image_256X256=image_256X256,image_512X512=image_512X512,image_1024X1024=image_1024X1024,image_2048X2048=image_2048X2048,identifier=response.id,createdate=timezone.now())
    return thumb.id

  
def generatemediadir(secret,contentid,filename,data):
    if not os.path.exists("website/static/"):
        os.mkdir("website/static")
    if not os.path.exists("website/static/media"):
        os.mkdir("website/static/media")
    if not os.path.exists("website/static/media/samples"):
        os.mkdir("website/static/media/samples")
    if not os.path.exists("website/static/media/live"):
        os.mkdir("website/static/media/live")
    if not os.path.exists("website/static/media/live/"+contentid):
        os.mkdir("website/static/media/live/"+contentid)
    fileinfo=filename.split(".")
    name=fileinfo[0]
    ext=fileinfo[1]
    fullname="website/static/media/live/"+contentid+"/"+name+"."+ext
    fullname_enc="website/static/media/live/"+contentid+"/"+name+"_encrypted."+ext
    fullname_new="website/static/media/live/"+contentid+"/"+name+"_new."+ext
    with open(fullname,"w+") as f:
            f.write(data)
    #f1=open(fullname,"r+")
    #f2=open(fullname_enc,"w+")
    try:
        #encrypt(f1, f2, secret, key_length=32)
        #encrypt_file(secret, fullname, fullname_enc, chunksize=64*1024)
        b64encrypt(secret, fullname, fullname_enc, chunksize=64*1024)
    except Exception as ex:
        print ex
    #f3=open(fullname_enc,"r+")
    #f4=open(fullname_new,"w+")
    #try:
        #decrypt(f3, f4, secret, key_length=32)
    #    decrypt_file(secret, fullname_enc, fullname_new, chunksize=24*1024)
    #except Exception as ex:
    #    print ex
    size=os.path.getsize(os.path.abspath(fullname_enc))
    fullurl=siteurl+"/static/media/live/"+contentid+"/"+name+"_encrypted."+ext
    Content.objects.create(identifier = contentid,url = fullurl,filename = filename,size = size,defaultkey = secret,uploaddate=timezone.now())
    
    

def randomgen(length):
       return ''.join(random.choice(string.lowercase) for i in range(length))



def verifySignature(req):
    request=req
    sig_verify={}
    if "HTTP_X_AP_SIGNATURE" not in request.META:
        sig_verify['status']="invalid signature"
    elif "HTTP_X_NL_API_VERSION" not in request.META:
        sig_verify['status']="unknown api version"
    elif "HTTP_VERSION" not in request.META:
        sig_verify['status']="unknown app version"
    elif "HTTP_X_NL_KEY" not in request.META:
        sig_verify['status']="invalid key"
    else:
        sig_verify['status']="ok"
    if sig_verify['status']!="ok":
        data={}
        data['status']="failed"
        data['message']=sig_verify['status']
    else:
        data={}
        data['status']="ok"
    data['status']="ok"
    return data