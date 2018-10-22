from __future__ import unicode_literals
import random
from django.db import models
from mongoengine import Document,EmbeddedDocument,EmbeddedDocumentField,FloatField,ReferenceField,StringField,IntField,ListField,DateTimeField,connect
from datetime import *
connect('fmw')


# Create your models here.
class License(models.Model):
    db_table = 'license'
    id = models.AutoField(primary_key=True)
    lkey = models.CharField(max_length=20)
    uid = models.IntegerField(default=0)
    pid = models.IntegerField(default=0)
    licensedate = models.DateTimeField('date created')

class Category(models.Model):
    db_table = 'category'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    createdate = models.DateTimeField('date created')

class SubCategory(models.Model):
    db_table = 'subcategory'
    id = models.AutoField(primary_key=True)
    categoryid = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    createdate = models.DateTimeField('date created')

class Collection(models.Model):
    db_table = 'category'
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")
    description = models.TextField(default="")
    createdate = models.DateTimeField('date created')

class Book(models.Model):
    db_table = 'category'
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")
    description = models.TextField(default="")
    authorid = models.IntegerField(default=0)
    isbn = models.CharField(max_length=50)
    publishdate = models.DateTimeField('date created')
    createdate = models.DateTimeField('date created')

class Chapter(models.Model):
    db_table = 'category'
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")
    bookid = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

class Author(models.Model):
    db_table = 'author'
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")
    uid = models.IntegerField(default=0)
    thumbid = models.IntegerField(default=0)
    joindate = models.DateTimeField('date created')


class Readby(models.Model):
    db_table = 'readby'
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")
    uid = models.IntegerField(default=0)
    thumbid = models.IntegerField(default=0)
    joindate = models.DateTimeField('date created')

class Product(models.Model):
    db_table = 'product'
    id = models.AutoField(primary_key=True)
    description = models.TextField(default="")
    thumbid = models.IntegerField(default=0)
    contentid = models.CharField(max_length=100)
    dccopyid = models.CharField(max_length=100)
    name = models.TextField(default="")
    catid = models.IntegerField(default=0)
    hassample = models.IntegerField(default=0)
    textid = models.IntegerField(default=0)
    authorid = models.IntegerField(default=0)
    readbyid = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=20,decimal_places=2)
    adddate = models.DateTimeField('date created')

class DCCopy(models.Model):
    db_table = 'content'
    id = models.AutoField(primary_key=True)
    identifier = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    size = models.IntegerField(default=0)
    defaultkey = models.CharField(max_length=200)
    uploaddate = models.DateTimeField('date uploaded')
	
class ProductStats(models.Model):
    db_table = 'productstats'
    id = models.AutoField(primary_key=True)
    pid = models.IntegerField(default=0)
    uid = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    listen = models.IntegerField(default=0)
    download = models.IntegerField(default=0)




class Subscriptions(models.Model):
    db_table = 'subscriptions'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    active = models.IntegerField(default=0)
    lastsubdate = models.DateTimeField('date last subscribed')
    nextsubdate = models.DateTimeField('date for next subscription')



class Transactions(models.Model):
    db_table = 'transactions'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    pid = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    tax = models.DecimalField(max_digits=20,decimal_places=2)
    description = models.TextField(default="")
    reference = models.CharField(max_length=100)
    otherref = models.CharField(max_length=100)
    commission = models.DecimalField(max_digits=20,decimal_places=2)
    voucher_code = models.CharField(max_length=20)
    status = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

class Purchases(models.Model):
    db_table = 'purchases'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    pid = models.IntegerField(default=0)
    comment = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    tax = models.DecimalField(max_digits=20,decimal_places=2)
    commission = models.DecimalField(max_digits=20,decimal_places=2)
    voucher_code = models.CharField(max_length=20)
    status = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

class Commission(models.Model):
    db_table = 'commission'
    id = models.AutoField(primary_key=True)
    pid = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    createdate = models.DateTimeField('date created')

class Admin(models.Model):
    db_table = 'admin'
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    role = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

class AdminRole(models.Model):
    db_table = 'adminrole'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    createdate = models.DateTimeField('date created')

class Wallet(models.Model):
    db_table = 'wallet'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=20,decimal_places=2)
    createdate = models.DateTimeField('date created')


class Voucher(models.Model):
    db_table = 'category'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    usedbyid = models.IntegerField(default=0)
    tid = models.IntegerField(default=0)
    vouchercode = models.TextField(default="")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')


class API(models.Model):
    db_table = 'api'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    apikey = models.CharField(max_length=20)
    apisecret = models.CharField(max_length=20)
    createdate = models.DateTimeField('date created')


class User(models.Model):
    db_table = 'user'
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    isphoneverified = models.IntegerField(default=0)
    isemailverified = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')


class UserLogin(models.Model):
    db_table = 'userlogin'
    id = models.AutoField(primary_key=True)
    deviceid = models.CharField(max_length=200)
    uid = models.IntegerField(default=0)
    ipaddress = models.CharField(max_length=500)
    latlong = models.CharField(max_length=200)
    createdate = models.DateTimeField('date created')



class Device(models.Model):
    db_table = 'device'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    fullname = models.CharField(max_length=500)
    uid = models.IntegerField(default=0)
    uuid = models.CharField(max_length=200)
    createdate = models.DateTimeField('date created')


class ForumTopic(models.Model):
    db_table = 'forumtopic'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    topic = models.CharField(max_length=500)
    image = models.TextField(max_length=1000)
    body = models.TextField(max_length=1000)
    comments = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    isactive = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

class ForumPost(models.Model):
    db_table = 'forumpost'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    topicid = models.IntegerField(default=0)
    body = models.TextField(default="")
    isactive = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

	
class ProductComment(models.Model):
    db_table = 'forumpost'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    productid = models.IntegerField(default=0)
    body = models.TextField(default="")
    isactive = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

class Promo(models.Model):
    db_table = 'promo'
    id = models.AutoField(primary_key=True)
    productid = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    promocode = models.TextField(default="")
    description = models.TextField(default="")
    isactive = models.IntegerField(default=0)
    startdate = models.DateTimeField('date started')
    enddate = models.DateTimeField('date ending')
    createdate = models.DateTimeField('date created')


class Message(models.Model):
    db_table = 'message'
    id = models.AutoField(primary_key=True)
    message = models.TextField(default="")
    links = models.TextField(default="")
    recepients = models.TextField(default="")
    createdate = models.DateTimeField('date created')


class Settings(models.Model):
    db_table = 'settings'
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")
    value = models.TextField(default="")
    description = models.TextField(default="")
    createdate = models.DateTimeField('date created')

class Profile(models.Model):
    db_table = 'profile'
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    profilepics = models.TextField(default="")
    biography = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.IntegerField(default=0)
    state = models.IntegerField(default=0)
    country = models.IntegerField(default=0)
    gender = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

class Thumbs(models.Model):
    db_table = 'thumbs'
    id = models.AutoField(primary_key=True)
    identifier = models.CharField(max_length=200)
    image_32X32 = models.CharField(max_length=200)
    image_64X64 = models.CharField(max_length=200)
    image_128X128 = models.CharField(max_length=200)
    image_256X256 = models.CharField(max_length=200)
    image_512X512 = models.CharField(max_length=200)
    image_1024X1024 = models.CharField(max_length=200)
    image_2048X2048 = models.CharField(max_length=200)
    createdate = models.DateTimeField('date created')

class Content(models.Model):
    db_table = 'content'
    id = models.AutoField(primary_key=True)
    identifier = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    sampleurl = models.CharField(max_length=1000)
    documenturl = models.CharField(max_length=1000)
    rdturl = models.CharField(max_length=1000)
    filename = models.CharField(max_length=200)
    size = models.IntegerField(default=0)
    defaultkey = models.CharField(max_length=200)
    uploaddate = models.DateTimeField('date uploaded')

###Mongodb storage models
class MongoProductStats(Document):
    productid = StringField(required=True, max_length=200)
    uid=IntField(required=True,default=0)
    rating=IntField(required=True,default=0)
    like=IntField(required=True,default=0)
    listen=IntField(required=True,default=0)
    downloads=IntField(required=True,default=0)
    updatedate = DateTimeField(default=datetime.utcnow)
    meta = {'allow_inheritance': True}
    
class ContentRating(Document):
    contentid = StringField(required=True, max_length=200)
    uid=IntField(required=True,default=0)
    like=IntField(required=True,default=0)
    listen=IntField(required=True,default=0)
    download=IntField(required=True,default=0)
    title = StringField(required=True, max_length=200)
    createdate = DateTimeField(default=datetime.utcnow)
    meta = {'allow_inheritance': True}


class UserFollow(Document):
    uid=IntField(required=True,default=0)
    username = StringField(required=True)
    profilepics = StringField(required=True)
    fid=IntField(required=True,default=0)
    fusername = StringField(required=True)
    fprofilepics = StringField(required=True)
    followdate = DateTimeField(default=datetime.utcnow)


class UserLikes(Document):
    uid=IntField(required=True,default=0)
    username = StringField(required=True)
    profilepics = StringField(required=True)
    mediaid=IntField(required=True,default=0)
    productname = StringField(required=True)
    productpic = StringField(required=True)
    likedate = DateTimeField(default=datetime.utcnow)

class UserRate(Document):
    uid=IntField(required=True,default=0)
    mediaid=IntField(required=True,default=0)
    score = FloatField(required=True)
    ratedate = DateTimeField(default=datetime.utcnow)

class Comment(Document):
    uid = IntField()
    topicid = IntField()
    username = StringField()
    text = StringField()
    image = StringField()
    profilepic = StringField()
    commentdate = DateTimeField(default=datetime.utcnow)

class Message(Document):
    topicid = IntField()
    comments = ListField(ReferenceField(Comment))



class BlogPost(Document):
    title = StringField(required=True, max_length=200)
    posted = DateTimeField(default=datetime.utcnow)
    tags = ListField(StringField(max_length=50))
    meta = {'allow_inheritance': True}

class TextPost(BlogPost):
    content = StringField(required=True)

class LinkPost(BlogPost):
    url = StringField(required=True)


def forumToJson(f):
    forums=[]
    for forum in f:
        data={}
        if forum.isactive==0:
            status="Disabled"
        else:
            status="Active"
        #data.append(forum.postedby)
        data['id']=forum.id
        data['topic']=forum.topic
        data['comments']=forum.comments
        data['likes']=forum.likes
        data['status']=status
        data['createdate']=forum.createdate
        forums.append(data)
    return forums


def postToJsonMobile(f):
    forums=[]
    for forum in f:
        data={}
        if forum.isactive==0:
            status="Disabled"
        else:
            status="Active"
        data['id']=forum.id
        data['uid']=forum.uid
        data['topic']=forum.topic
        data['body']=forum.body
        data['username']=forum.username
        data['comments']=forum.comments
        data['likes']=forum.likes
        data['postdate']=forum.postdate
        forums.append(data)
    return forums


def adminToJson(a):
    users=[]
    for admin in a:
        data={}
        if admin.status==0:
            status="Disabled"
        else:
            status="Active"
        data['id']=admin.id
        data['username']=admin.username
        data['role']=admin.role
        data['status']=status
        users.append(data)
    return users

def usersToJson(u):
    users=[]
    for user in u:
        data={}
        if user.status==0:
            status="Disabled"
        else:
            status="Active"
        data['id']=user.id
        data['username']=user.username
        data['fullname']=user.firstname+" "+user.lastname
        data['email']=user.email
        data['telephone']=user.telephone
        data['email'] = user.email
        data['address'] = user.address
        data['city'] = user.city
        data['state'] = user.state
        data['country'] = user.country
        data['isphoneverified']=user.isphoneverified
        data['isemailverified']=user.isemailverified
        data['status']=status
        data['createdate']=user.createdate
        users.append(data)
    return users



def subscriptionsToJson(u):
    subscriptions=[]
    for subscription in u:
        data={}
        if subscription.status==0:
            status="Disabled"
        else:
            status="Active"
        data['id']=subscription.id
        data['username']=subscription.username
        data['fullname']=subscription.firstname+" "+subscription.lastname
        data['email']=subscription.email
        data['telephone']=subscription.telephone
        data['email'] = subscription.email
        data['address'] = subscription.address
        data['city'] = subscription.city
        data['state'] = subscription.state
        data['country'] = subscription.country
        data['isphoneverified']=subscription.isphoneverified
        data['isemailverified']=subscription.isemailverified
        data['status']=status
        data['active']=subscription.active
        data['nextsubdate'] = subscription.nextsubdate
        data['lastsubdate'] = subscription.lastsubdate
        data['createdate'] = subscription.createdate

        subscriptions.append(data)
    return subscriptions

def booksToJson(b):
    books=[]
    for book in b:
        data={}
        data['id']=book.id
        data['name']=book.name
        data['isbn']=book.isbn
        data['author']=book.author
        data['description']=book.description
        data['publishdate']=book.publishdate
        data['createdate']=book.createdate
        books.append(data)
    return books


def getBookDict(b):
    books=[]
    for book in b:
        data={}
        data['id']=book.id
        data['name']=book.name
        data['isbn']=book.isbn
        data['author']=book.author
        data['description']=book.description
        data['publishdate']=book.publishdate
        data['createdate']=book.createdate
        books.append(data)
    return books


def productToJson(siteurl,p):
    products=[]
    for product in p:
        data={}
        data['id']=product.id
        data['name']=product.product
        data['category']=product.category
        data['author']=product.author
        data['documenturl']=siteurl+"/"+product.documenturl
        data['audiourl'] = siteurl+"/"+product.url
        data['sampleurl'] = siteurl+"/"+product.sampleurl
        data['description'] = product.description
        data['price']=product.price
        data['image']=siteurl+"/"+product.image
        products.append(data)
    return products

def productToJsonMobile(siteurl,p):
    products=[]
    for product in p:
        #print p
        data={}
        data['id']=product.id
        data['name']=product.product
        data['category']=product.category
        data['author'] = product.author
        data['description'] = product.description
        data['price'] = product.price
        #prating=ContentRating.objects(contentid=product.id)
        data['likes']=random.randint(0,5)
        data['listen']=random.randint(0,5)
        data['downloads']=random.randint(0,5)
        data['duration']=0
        if product.duration!=None:
            data['duration'] = product.duration
        data['readby']="Not Available"
        try:
            readbyid=product.readbyid
            readby = Readby.objects.get(id=readbyid)
            data['readby'] = readby.name
        except Exception as ex:
            data['readby'] = "Not Available"

        data['publishdate']="Not Available"
        if product.adddate!=None:
            data['publishdate'] = product.adddate
        #data['size']=product.size
        if product.image!=None:
            if "http" in product.image:
                data['image']=product.image
            else:
                if "static" in product.image:
                    data['image']=siteurl+"/"+product.image
                else:
                    data['image'] = siteurl + "/static/thumbs/" + product.image
        else:
            data['image']=siteurl+"/static/thumbs/icon.png"
        if product.image2!=None:
            if "http" in product.image2:
                data['image2']=product.image2
            else:
                if "static" in product.image2:
                    data['image2']=siteurl+"/"+product.image2
                else:
                    data['image2'] = siteurl + "/static/thumbs/" + product.image2
        else:
            data['image2']=siteurl+"/static/thumbs/icon.png"
        if product.image3!=None:
            if "http" in product.image3:
                data['image3']=product.image3
            else:
                if "static" in product.image3:
                    data['image3']=siteurl+"/"+product.image3
                else:
                    data['image3'] = siteurl + "/static/thumbs/" + product.image3
        else:
            data['image3']=siteurl+"/static/thumbs/icon.png"
        products.append(data)
    return products

 

def authorsToJson(a):
    authors=[]
    for author in a:
        data={}
        data["id"]=author.id 
        data["name"]=author.name
        if author.image==None:
            data['image']="static/thumbs/icon.png"
        else:
            if "http" in author.image:
                data['image']=author.image
            else:
                data["image"]=author.image
        data["date"]=author.joindate
        authors.append(data)
    return authors


def authorsToJsonMobile(siteurl,a):
    authors=[]
    for author in a:
        data={}
        data["id"]=author.id 
        data["name"]=author.name
        if author.image==None:
            data['image']="static/thumbs/icon.png"
        else:
            if "http" in author.image:
                data['image']=author.image
            else:
                data["image"]=siteurl+"/"+author.image
        data["date"]=author.joindate
        authors.append(data)
    return authors


def topicsToJsonMobile(siteurl,f):
    forums=[]
    for forum in f:
        data={}
        if forum.isactive==0:
            status="false"
        else:
            status="true"
        #data.append(forum.postedby)
        data['id']=forum.id
        data['uid']=forum.uid
        data['topic']=forum.topic
        data['image']=forum.image
        data['body']=forum.body
        data['comments']=forum.comments
        data['likes']=forum.likes
        data['isactive']=status
        data['createdate']=forum.createdate
        forums.append(data)
    return forums


def licensesToJson(a):
    licenses=[]
    for license in a:
        data={}
        data["id"]=license.id 
        data["username"]=license.username
        data["key"]=license.lkey
        data["product"]=license.product
        data["licensedate"]=license.licensedate
        licenses.append(data)
    return licenses

def transactionsToJson(a):
    transactions=[]
    for transaction in a:
        data={}
        data["id"]=transaction.id
        data["name"]=transaction.name
        if transaction.image==None:
            data['image']="static/thumbs/icon.png"
        else:
            data["image"]="static/thumbs/"+transaction.image
        data["date"]=transaction.joindate
        transactions.append(data)
    return transactions

def getCategoryDict(categories):
    categorylist=[]
    for c in categories:
        data={}
        data['name']=c.name
        data['id']=c.id
        categorylist.append(data)

    return categorylist

def getProductDict(products):
    productlist=[]
    for p in products:
        data={}
        data['name']=p.name
        data['id']=p.id
        data['authorid']=p.authorid
        data['price']=p.price
        data['adddate']=p.adddate
        data['description']=p.description
        productlist.append(data)

    return productlist

def getPurchaseDict(product,purchase,content,author):
    productlist=[]
    data={}
    data['name']=product.name
    data['id']=product.id
    data['author']=author.name
    data['price']=product.price
    data['adddate']=product.adddate
    data['description']=product.description
    data['mediaid']=product.contentid
    data['filename']=content.filename
    data['url']=content.url
    data['defaultkey']=content.defaultkey
    data['size']=content.size
    productlist.append(data)

    return productlist

def getPurchasesDict(purchases):
    purchaselist=[]
    for p in purchases:
        data={}
        data['name']=p.name
        data['id']=p.id
        data['author']=p.author
        data['price']=p.price
        data['purchasedate']=p.purchasedate
        data['adddate']=p.adddate
        data['description']=p.description
        data['mediaid']=p.contentid
        data['filename']=p.filename
        data['url']=p.url
        data['defaultkey']=p.defaultkey
        data['size']=p.size
        purchaselist.append(data)

    return purchaselist


def PurchasesToJson(purchases):
    purchaselist=[]
    for p in purchases:
        data={}
        data['item']=p.productname
        data['id']=p.id
        data['price']=p.price
        data['username']=p.username
        data['commission']=p.commission
        data['voucher_code']=p.voucher_code
        data['status']=p.status
        data['purchasedate']=p.purchasedate
        purchaselist.append(data)

    return purchaselist


def promoToJsonMobile(promos):
    promolist=[]
    for p in promos:
        data={}
        data['promocode']=p.promocode
        data['id']=p.id
        data['startdate']=p.startdate
        data['enddate']=p.enddate
        data['product']=p.product
        data['productdescription']=p.productdescription
        data['promodescription']=p.promodescription
        data['price']=p.price
        data['thumbid']=p.thumbid
        data['image']=p.image
        data['status'] = p.status
        data['createdate'] = p.createdate
        promolist.append(data)

    return promolist


def getPurchaseSync(siteurl,purchases,purchaseids):
    purchaselist=[]
    for p in purchases:
        data={}
        data['availablelocally'] = 0
        if isAvailableLocally(purchaseids,p.id):
            data['availablelocally']=1
        data['id']=p.id
        data['purchasedate']=p.purchasedate
        data['pid']=p.pid
        data['comment']=p.comment
        data['amount']=p.amount
        data['tax']=p.tax
        data['commission']=p.commission
        data['voucher_code']=p.voucher_code
        data['status']=p.status
        data['uid'] = p.uid
        data['description'] = p.description
        data['thumbid'] = p.thumbid
        data['name']=p.product
        data['catid'] = p.catid
        data['author'] = p.author
        data['price'] = p.price
        data['adddate'] = p.adddate
        data['contentid'] = p.contentid
        data['image']=[]
        if p.image_32X32!=None:
            data['image'].append({"id":1,"url":siteurl+"/"+p.image_32X32})
        if p.image_64X64 != None:
            data['image'].append({"id":2,"url":siteurl+"/"+p.image_64X64})
        if p.image_128X128 != None:
            data['image'].append({"id":3,"url":siteurl+"/"+p.image_128X128})
        if p.image_256X256 != None:
            data['image'].append({"id":4,"url":siteurl+"/"+p.image_256X256})
        if p.image_512X512 != None:
            data['image'].append({"id":5,"url":siteurl+"/"+p.image_512X512})
        if p.image_1024X1024 != None:
            data['image'].append({"id":6,"url":siteurl+"/"+p.image_1024X1024})
        if p.image_2048X2048 != None:
            data['image'].append({"id":7,"url":siteurl+"/"+p.image_2048X2048})
        data['identifier'] = p.identifier
        data['url'] = siteurl+"/"+p.url
        data['size'] = p.size
        data['duration'] = p.duration
        data['defaultkey'] = p.defaultkey
        data['uploaddate'] = p.uploaddate
        data['rdturl'] =""
        if p.rdturl!=None:
            data['rdturl'] = siteurl+"/"+p.rdturl
        data['filename'] = siteurl+"/"+p.filename
        purchaselist.append(data)

    return purchaselist

def categoryToJson(c):
    categories=[]
    for cat in c:
        data={}
        data["id"]=cat.subcatid
        data["name"]=cat.catname
        data["subcategory"] = cat.subcatname
        data["date"]=cat.catdate
        categories.append(data)
    return categories


def subCategoryToJson(c):
    subcategories=[]
    for subcat in c:
        data={}
        data["id"]=subcat.id
        data["categoryid"] = subcat.categoryid
        data["name"]=subcat.name
        data["date"]=subcat.createdate
        subcategories.append(data)
    return subcategories

def walletToJson(w):
    wallets=[]
    for wallet in w:
        data={}
        data['id']=wallet.id
        data['username']=wallet.username
        data['balance']=wallet.balance
        data['createdate']=wallet.createdate
        wallets.append(data)
    return wallets


def sampleToJson(siteurl,product):
    data={}
    data["id"]=product[0].id
    data["name"]=product[0].name
    data["url"]=siteurl+"/"+product[0].sampleurl
    return data


def userToJsonMobile(users):
    userlist=[]
    for user in users:
        data={}
        data['username']=user.username
        data['profilepic']=user.profilepics
        data['fullname']=user.firstname+ " "+user.lastname
        data['uid']=user.uid
        userlist.append(data)
    return userlist



def userToJsonMobile2(uid,users):
    userlist=[]
    import time
    for user in users:
        data={}
        starttime=time.time()
        print "My Id "+str(uid)+" Follower "+str(user.id)
        userfollow=UserFollow.objects(uid=uid,fid=user.id)
        data['following'] = False
        if len(userfollow)>0:
            data['following']=True
        data['username']=user.username
        data['profilepic']=user.profilepics
        data['firstname']=user.firstname
        data['lastname'] = user.lastname
        data['uid']=user.id
        userlist.append(data)
        endtime= time.time()-starttime
        print "Completed in %d",endtime
    return userlist


def documentToJson(siteurl,product):
    data={}
    data["id"]=product[0].id
    data["name"]=product[0].name
    data["url"]=siteurl+"/"+product[0].documenturl
    return data

def isAvailableLocally(purchaseids,pid):
    for p in purchaseids:
        if p == pid:
            return True

    return False

def productpostToJsonMobile(posts):
    post=[]
    for p in posts:
        data={}
        data['id']=p.id
        data['body']=p.body
        data['username']=p.username
        data['name']=p.name
        data['postdate']=p.postdate
        post.append(data)
    return post
