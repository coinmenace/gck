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
from thumbgen import *
from task import *
from aesutil import *
# Create your views here.
from django.contrib.gis.geoip import GeoIP
import messages
import settings
from tinytag import TinyTag
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import pyminizip
import json
import redis
rdb = redis.Redis()
# Create your views here.
siteurl=settings.siteurl
data={"sitename":"MyRidit"}



def generateauthordir():
    if not os.path.exists("static/"):
        os.mkdir("static")
    if not os.path.exists("static/authors"):
        os.mkdir("static/authors")
    if not os.path.exists("static/authors/thumb"):
        os.mkdir("static/authors/thumb")

def generatethumbs(poster):
    if not os.path.exists("static/thumbs"):
        os.mkdir("static/thumbs/")
    if not os.path.exists("static/thumbs/tmp"):
        os.mkdir("static/thumbs/tmp/")
    print poster.name
    data=poster.read()
    print "File size %d  ",len(data)
    with open("static/thumbs/tmp/"+poster.name,"w+") as f:
        f.write(data)
        f.close()
    result={}
    result['uploaddir']="static/thumbs/"
    result['fullname']="static/thumbs/tmp/"+poster.name
    result['file']=poster.name
    response=generateImageThumbNails.delay(result)
    identifier=response.id
    filename=poster.name.split(".")[0]
    image_32X32="static/thumbs/"+identifier+"/"+filename+"_32_32.png"
    image_64X64="static/thumbs/"+identifier+"/"+filename+"_64_64.png"
    image_128X128="static/thumbs/"+identifier+"/"+filename+"_128_128.png"
    image_256X256="static/thumbs/"+identifier+"/"+filename+"_256_256.png"
    image_512X512="static/thumbs/"+identifier+"/"+filename+"_512_512.png"
    image_1024X1024="static/thumbs/"+identifier+"/"+filename+"_1024_1024.png"
    image_2048X2048="static/thumbs/"+identifier+"/"+filename+"_2048_2048.png"
    thumb=Thumbs.objects.create(image_32X32=image_32X32,image_64X64=image_64X64,image_128X128=image_128X128,image_256X256=image_256X256,image_512X512=image_512X512,image_1024X1024=image_1024X1024,image_2048X2048=image_2048X2048,identifier=response.id,createdate=timezone.now())
    thumbdata =[]
    thumbdata.append(thumb.id)
    thumbdata.append(image_512X512)
    return thumbdata


def generatemediadir(generatesample,duration,secret,contentid,filename,data,document):
    outdata=[]
    if not os.path.exists("static/"):
        os.mkdir("static")
    if document!=None:
        documentfullname = processDocument(document,contentid)
        print documentfullname
        print contentid
        outdata.append(documentfullname)
        try:
            if documentfullname!=None:
                content = Content.objects.get(identifier=contentid)
                content.documenturl = documentfullname
                content.save()
        except Exception as ex:
            print ex
    if data != None:
        if not os.path.exists("static/media"):
            os.mkdir("static/media")
        if not os.path.exists("static/media/samples"):
            os.mkdir("static/media/samples")
        if not os.path.exists("static/media/samples/"+contentid):
            os.mkdir("static/media/samples/"+contentid)
        if not os.path.exists("static/media/live"):
            os.mkdir("static/media/live")
        if not os.path.exists("static/media/live/"+contentid):
            os.mkdir("static/media/live/"+contentid)
        fileinfo=filename.split(".")
        ext=fileinfo[len(fileinfo)-1]
        name=filename.replace("."+ext,"")
        fullname="static/media/live/"+contentid+"/"+name+"."+ext
        fullname_enc="static/media/live/"+contentid+"/"+name+"_encrypted."+ext
        fullname_new="static/media/live/"+contentid+"/"+name+"_new."+ext
        with open(fullname,"w+") as f:
                f.write(data)
        if generatesample==1:
            samplefile = "static/media/samples/" + contentid + "/" + name + "." + ext
            if duration>0:
                command='ffmpeg -t '+str(duration)+' -i "'+fullname+'" -acodec copy "'+samplefile+'"'
                print command
                os.system(command)
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
        fullurl="static/media/live/"+contentid+"/"+name+"_encrypted."+ext
        filename="static/media/live/"+contentid+"/"+name+"."+ext
        sampleurl=""
        if generatesample==1:
            sampleurl = "static/media/samples/" + contentid + "/" + name + "." + ext
            #sampleurl = siteurl + "/static/media/samples/" + contentid + "/" + name + "_encrypted." + ext
        print sampleurl
        tag = TinyTag.get(filename)
        fileduration = tag.duration
        content = Content.objects.create(identifier = contentid,url = fullurl,sampleurl=sampleurl,documenturl = documentfullname ,filename = filename,size = size,defaultkey = secret,uploaddate=timezone.now())
        outdata.append(filename)
        outdata.append(fileduration)
        print "Content ID "+str(content.id)
        return outdata


def processDocument(document,contentid):
    docfullname = ""
    try:
        if document != None:
            if not os.path.exists("static/documents"):
                os.mkdir("static/documents")
            if not os.path.exists("static/documents/" + contentid):
                os.mkdir("static/documents/" + contentid)
                docfilename = document.name
                docdata = document.read()
                docfileinfo = docfilename.split(".")
                docext = docfileinfo[len(docfileinfo) - 1]
                docname = docfilename.replace("."+docext,"")
                docfullname = "static/documents/" + contentid + "/" + docname + "." + docext
                with open(docfullname, "w+") as f:
                    f.write(docdata)
    except Exception as ex:
        docfullname = ""
        print ex
    print "Document full name  "+docfullname
    return docfullname

def randomgen(length):
       return ''.join(random.choice(string.lowercase) for i in range(length))

