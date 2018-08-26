# -*- coding: utf-8 -*-
from celery import task, current_task,subtask,group
from celery import current_app
import time,random
import json
from os import listdir
from os.path import isfile, join
from django.db.models import Q
import PIL
from PIL import Image
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from mp3tag import *
from thumbgen import *
@task
def generateImageThumbNails(results):
		i=1
		task_id=generateImageThumbNails.request.id
		fullname=results['fullname']
		file=results['file']
		t=Thumbgen(file,fullname,task_id)
		status="COMPLETE"
		os.remove(fullname)
		accountlist=[]
		

@task
def signMp3File(results):
		i=1
		task_id=requestProfileStats.request.id
		#print "Task ID "+task_id
		status="COMPLETE"
		accountlist=[]
		print results
	    #meta={'current': len(results), 'total': len(results),'data':accountlist,'status':status}
		#redis_publisher = RedisPublisher(facility='getprofile', broadcast=True)
		#message = RedisMessage(json.dumps(accounts))
		#redis_publisher.publish_message(message)
		#current_app.backend.store_result(task_id,meta,status)
		#current_task.update_state(state=status,meta=meta)
		#return accountlist