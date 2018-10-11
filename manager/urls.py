'''
Created on October 6, 2016

@author: adebayoolabode
'''

from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'admin/list', views.listadmin, name='listadmin'),
url(r'admin/delete/(?P<id>\d+)', views.deleteadmin, name='deleteadmin'),
url(r'admin/createrole', views.createadminrole, name='createadminrole'),
url(r'admin/create', views.createadmin, name='createadmin'),
url(r'admin/update', views.updateadmin, name='updateadmin'),
url(r'admin', views.admin, name='admin'),
url(r'wallet/usercredit/(?P<id>\d+)', views.viewcreditwallet, name='viewcreditwallet'),
url(r'wallet/userdebit/(?P<id>\d+)', views.viewdebitwallet, name='viewdebitwallet'),
url(r'wallet/credit', views.creditwallet, name='creditwallet'),
url(r'wallet/debit', views.debitwallet, name='debitwallet'),
url(r'wallet/list', views.listwallet, name='listwallet'),
url(r'wallet/delete/(?P<id>\d+)', views.deletewallet, name='deletewallet'),
url(r'wallet', views.wallet, name='wallet'),

url(r'banner/create', views.createbanner, name='createbanner'),
url(r'banner/list', views.listbanner, name='listbanner'),
url(r'banner/delete/(?P<id>\d+)', views.deletebanner, name='deletebanner'),
url(r'banner/edit', views.updatebanner, name='updatebanner'),

url(r'banner', views.banner, name='banner'),



url(r'books/createcollection', views.createcollection, name='createcollection'),
url(r'books/deletecollection/(?P<id>\d+)', views.deletecollection, name='deletecollection'),
url(r'books/create', views.createbook, name='createbook'),
url(r'books/list', views.listbook, name='listbook'),
url(r'books/delete/(?P<id>\d+)', views.deletebook, name='deletebook'),
url(r'books/edit', views.index, name='log'),

url(r'books', views.books, name='content'),



url(r'subscriptions/list', views.listsubscriptions, name='listsubscriptions'),

url(r'users/create', views.createuser, name='createuser'),
url(r'users/list', views.listusers, name='listusers'),
url(r'users/delete/(?P<id>\d+)', views.deleteuser, name='deleteuser'),
url(r'users/resetdevice/(?P<id>\d+)', views.resetuserdevice, name='resetuserdevice'),
url(r'users/update', views.updateuser, name='updateuser'),
url(r'users', views.users, name='users'),

url(r'authors/create', views.createauthor, name='createauthor'),
url(r'authors/list', views.listauthors, name='listauthors'),
url(r'authors/delete/(?P<id>\d+)', views.deleteauthors, name='deleteauthors'),
url(r'authors/update', views.updateauthor, name='updateauthor'),
url(r'authors', views.authors, name='authors'),



url(r'subcategory/create', views.createsubcategory, name='createsubcategory'),
url(r'subcategory/list', views.listsubcategory, name='listsubcategory'),
url(r'subcategory/delete/(?P<id>\d+)', views.deletesubcategory, name='deletesubcategory'),
url(r'subcategory/update', views.updatesubcategory, name='updatesubcategory'),


url(r'category/create', views.createcategory, name='createcategory'),
url(r'category/list', views.listcategory, name='listcategory'),
url(r'category/delete/(?P<id>\d+)', views.deletecategory, name='deletecategory'),
url(r'category/update', views.updatecategory, name='updatecategory'),
url(r'categories', views.index, name='log'),




url(r'media/create', views.uploadcontent, name='uploadcontent'),
url(r'media/list', views.listmedia, name='listmedia'),
url(r'media/delete/(?P<id>\d+)', views.deletemedia, name='deletemedia'),
url(r'media/generate/(?P<id>\d+)', views.regeneratecontent, name='regeneratecontent'),
url(r'media/update', views.uploadcontent, name='uploadcontent'),

url(r'content', views.content, name='content'),

url(r'license/create', views.index, name='log'),
url(r'license/list', views.listlicenses, name='listlicenses'),
url(r'license/delete/(?P<id>\d+)', views.deletelicenses, name='deletelicenses'),
url(r'license/edit', views.index, name='log'),
url(r'license', views.license, name='license'),

url(r'forums/create', views.createforumtopic, name='createforumtopic'),
url(r'forums/list', views.listforums, name='listforums'),
url(r'forums/delete/(?P<id>\d+)', views.deleteforums, name='deleteforums'),
url(r'forums/edit', views.index, name='log'),
url(r'forums', views.forums, name='forums'),

url(r'promo/create', views.createpromo, name='createforumtopic'),
url(r'promo/list', views.listpromo, name='listforums'),
url(r'promo/delete/(?P<id>\d+)', views.deletepromo, name='deleteforums'),
url(r'promo/edit', views.index, name='log'),
url(r'promo', views.promo, name='promo'),

url(r'messages/create', views.createforumtopic, name='createforumtopic'),
url(r'messages/list', views.listforums, name='listforums'),
url(r'messages/delete/(?P<id>\d+)', views.deleteforums, name='deleteforums'),
url(r'messages/edit', views.index, name='log'),
url(r'messages', views.messages, name='messages'),


url(r'settings/create', views.createforumtopic, name='createforumtopic'),
url(r'settings/list', views.listforums, name='listforums'),
url(r'settings/delete/(?P<id>\d+)', views.deleteforums, name='deleteforums'),
url(r'settings/edit', views.index, name='log'),
url(r'settings', views.settings, name='settings'),

url(r'transactions/delete', views.index, name='log'),
url(r'transactions/list', views.listtransactions, name='listtransactions'),
url(r'transactions', views.transactions, name='transactions'),

url(r'login', views.login, name='login'),

url(r'auth', views.auth, name='auth'),

url(r'pushmessage', views.pushmessage, name='pushmessage'),

url(r'logout', views.logout, name='logout'),
]
