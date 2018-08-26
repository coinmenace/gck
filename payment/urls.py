'''
Created on October 6, 2016

@author: adebayoolabode
'''

from django.conf.urls import url
from . import views
urlpatterns = [
url(r'completed', views.paymentcompleted, name='paymentcompleted'),
url(r'process', views.dopay, name='dopay'),

url(r'home', views.index, name='index'),
]