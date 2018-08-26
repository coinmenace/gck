from admin import *
from authors import *
from books import *
from category import *
from collections import *
from content import *
from forums import *
from license import *
from login import *
from main import *
from transactions import *
from users import *
from wallet import *
from promo import *
from banners import *



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