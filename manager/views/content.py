# -*- coding: utf-8 -*-
from imports import *


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

def uploadcontent(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            productid = request.POST.get("productid")
            name=request.POST.get("name")
            catid=request.POST.get("catid")
            authorid=request.POST.get("authorid")
            description=request.POST.get("description")
            fulltext = request.POST.get("fulltext")
            readby = request.POST.get("readby")
            duration = request.POST.get("duration")
            price=request.POST.get("price")
            sample = request.POST.get("sample")
            generatesample=0
            duration=0
            if productid!=None:
                contentid = Product.objects.get(id=productid).contentid
            else:
                contentid = str(uuid.uuid4())
            if sample=="on":
                generatesample=1
                if request.POST.get("duration")=="":
                    duration = 0
                else:
                    duration = int(request.POST.get("duration"))
            readbyid = 0
            try:
                readbyid = Readby.objects.get(name=readby)
                if readbyid==None:
                    readbyid = Readby.objects.create(name= readby,uid=0,thumbid=0,joindate = timezone.now())
            except Exception as ex:
                print ex

            try:
                print request.FILES
                poster=request.FILES["poster"]
                imagefile =""
                thumbdata=generatethumbs(poster)
                thumbid = thumbdata[0]
                imagefile = thumbdata[1]
            except Exception as ex:
                thumbid=0
                print ex

            try:
                file=request.FILES["media"]
                filename=file.name
                data=file.read()

                document = request.FILES["document"]
                #fullname="website/static/media/samples/"+filename
                #fullname="website/static/media/live/"+filename
                secret=randomgen(16)
                documentfile=""
                audiofile = ""
                outputfile ="static/rdt/"+contentid+".rdt"
                outdata = generatemediadir(generatesample,duration,secret,contentid,filename,data,document)
                documentfile = outdata[0]
                audiofile = outdata[1]
                duration = outdata[2]
                print outdata
                try:
                    #secret ="admin234"
                    generatePackage(imagefile, documentfile, audiofile, outputfile, secret,contentid)
                except Exception as ex:
                    print ex
                textid=0
                if fulltext!=None:
                    if len(fulltext)>10:
                        contenttext=ContentText.objects.create(fulltext=fulltext)
                        textid=contenttext.id
            except Exception as ex:
                print ex
                textid = None
            product=processContent(name,thumbid,generatesample,readbyid,duration,contentid,catid,authorid,description,textid,price,productid)
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



def listmedia(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        query = "SELECT image_256X256 as image,product.id as id,category,author,product,description,price,documenturl,rdturl,sampleurl,url,contentid,defaultkey from (SELECT  api_product.id as id,api_category.name as category,api_author.name as author,api_product.name as product,description,price,api_product.thumbid as thumbid,contentid,identifier,documenturl,rdturl,sampleurl,url,defaultkey from api_product,api_category,api_author,api_content  WHERE api_content.identifier = api_product.contentid AND  api_product.authorid=api_author.id AND api_product.catid=api_category.id) as product left join api_thumbs as thumbs on product.thumbid=thumbs.id ORDER BY product.id DESC "+pager
        print query
        media=Product.objects.raw(query)
        data={}
        data['total']= Product.objects.count()
        siteurl = settings.siteurl
        data['rows']=productToJson(siteurl,media)
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


def regeneratecontent(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            mediaid=request.GET['id']
        else:
            mediaid=id
        product = Product.objects.filter(Q(id=mediaid))
        contentid = product[0].contentid
        thumbid = product[0].thumbid
        content = Content.objects.filter(Q(identifier = contentid))
        secret =  content[0].defaultkey
        documentfile = content[0].documenturl
        audiofile =  content[0].filename
        thumb = Thumbs.objects.filter(Q(id = thumbid))
        imagefile =  thumb[0].image_64X64
        outputfile = "static/rdt/" + contentid + ".rdt"
        print secret
        thread  = Thread(target=generatePackage,args =(imagefile, documentfile, audiofile, outputfile, secret, contentid))
        thread.start()
        return HttpResponseRedirect("../../content")
    else:
        return HttpResponseRedirect("login")


def processContent(name,thumbid,generatesample,readbyid,duration,contentid,catid,authorid,description,textid,price,productid=None):
    #print name,thumbid,generatesample,readbyid,duration,contentid,catid,authorid,description,textid,price,productid
    if productid == None:
        try:
            product = Product.objects.create(name=name, readbyid=readbyid,duration=duration,thumbid=thumbid, hassample=generatesample, contentid=contentid,catid=catid, authorid=authorid, description=description, textid=textid,price=price, adddate=timezone.now())
            print "Product ID "+str(product.id)
        except Exception as ex:
            product = None
            print ex
    else:
        try:
            product = Product.objects.get(id=productid)
            if name !=None and name!="":
                product.name = name
            if readbyid!=None and readbyid!="":
                product.readbyid = readbyid
            if duration!=None and duration!="":
                product.duration = duration
            if thumbid!=None and thumbid!=0:
                product.thumbid = thumbid
            if generatesample!=None and generatesample!="":
                product.hassample = generatesample
            if contentid!=None and contentid!="":
                product.contentid = contentid
            if catid!=None and catid!="":
                product.catid = catid
            if authorid!=None and authorid!="":
                product.authorid = authorid
            if description!=None and description!="":
                product.description = description
            if textid!=None and textid!="":
                product.textid = textid
            if price!=None and price!="":
                product.price = price
            product.save()
        except Exception as ex:
            product = None
            print ex
    return product



def generatePackage(imagefile,documentfile,audiofile,outputfile,secret,identifier):
    if not os.path.exists("static/rdt"):
        os.mkdir("static/rdt/")
    inputfiles =[]
    inputfiles.append(imagefile)
    inputfiles.append(documentfile)
    inputfiles.append(audiofile)
    print inputfiles
    try:
        pyminizip.compress_multiple(inputfiles, outputfile, secret, 5)
    except Exception as ex:
        print ex
    content = Content.objects.get(identifier = identifier)
    if content !=None:
        content.rdturl =  outputfile
        content.save()
    print "Done generating rdt file"