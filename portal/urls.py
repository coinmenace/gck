'''
Created on October 6, 2016

@author: adebayoolabode
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

]