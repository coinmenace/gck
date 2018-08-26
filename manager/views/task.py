# -*- coding: utf-8 -*-
from celery import task
import os
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
		#task_id=requestProfileStats.request.id
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

@task
def generateSample(results):
	inputpath=results['srcpath']
	outputpath=results['destinationpath']
	duration=results['duration']
	command="ffmpeg -t "+duration+" -i "+inputpath+" -acodec copy "+outputpath
	os.system(command)
	#current_app.backend.store_result(task_id,meta,status)
	#current_task.update_state(state=status,meta=meta)
	pass