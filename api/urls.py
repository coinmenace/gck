'''
Created on October 6, 2016

@author: adebayoolabode
'''

from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'v1/token', views.index, name='index'),
url(r'v1/stats', views.stats, name='index'),
url(r'v1/register', views.registeruser, name='registeruser'),
url(r'v1/devicelog', views.index, name='devicelog'),
url(r'v1/log', views.index, name='log'),
url(r'v1/authors', views.listauthors, name='listauthors'),
url(r'v1/forums', views.listforums, name='listforums'),
url(r'v1/auth', views.auth, name='auth'),
url(r'v1/resetpass', views.resetpass, name='resetpass'),
url(r'v1/changepass', views.changepass, name='changepass'),
url(r'v1/categories', views.listcategories, name='listcategories'),
url(r'v1/multiverify', views.multiverifydevice, name='multiverifydevice'),
url(r'v1/verify', views.verifydevice, name='verifydevice'),
url(r'v1/like/(?P<mediaid>\d+)/', views.dolike, name='dolike'),
url(r'v1/listen/(?P<mediaid>\d+)/', views.dolisten, name='dolisten'),
url(r'v1/user', views.index, name='user'),
url(r'v1/purchase/list', views.getpurchases, name='getpurchases'),
url(r'v1/purchase', views.purchase, name='purchase'),
url(r'v1/payment/completed', views.paymentcompleted, name='paymentcompleted'),
url(r'v1/payment', views.payment, name='payment'),
url(r'v1/rate', views.rate, name='rate'),
url(r'v1/productsbyid/(?P<productid>\d+)/', views.listproductswithid, name='listproductswithid'),
url(r'v1/products/(?P<catid>\d+)/(?P<page>\d+)/', views.listproducts, name='listproducts'),
url(r'v1/productcomment', views.productcomment, name='productcomment'),
url(r'v1/product/like', views.likeproduct, name='likeproduct'),
url(r'v1/product/unlike', views.unlikeproduct, name='unlikeproduct'),
url(r'v1/product/rate', views.rateproduct, name='rateproduct'),
url(r'v1/product/listen', views.updatelistens, name='updatelistens'),
url(r'v1/product/listcomment/(?P<pid>\d+)/(?P<page>\d+)/', views.listproductcomment, name='listcomment'),
url(r'v1/product/listrelated/(?P<catid>\d+)', views.listrelatedproducts, name='listrelated'),
url(r'v1/product/dlownload', views.updatedownloads, name='updatedownloads'),
url(r'v1/listproductcomment/(?P<productid>\d+)/(?P<page>\d+)', views.listproductcomment, name='listproductcomment'),
url(r'v1/search/product', views.searchproducts, name='searchproducts'),
url(r'v1/search/user', views.searchusers, name='searchusers'),
url(r'v1/authors', views.listauthors, name='listauthors'),
url(r'v1/publishers', views.index, name='publishers'),
url(r'v1/topics', views.index, name='topics'),
url(r'v1/listpost/(?P<topic>\d+)/(?P<page>\d+)/', views.listpost, name='listpost'),
url(r'v1/comment', views.postcomment, name='postcomment'),
url(r'v1/getprofile', views.getprofile, name='getprofile'),
url(r'v1/profile/picture', views.updateprofilepicture, name='updateprofilepicture'),
url(r'v1/license_validate', views.index, name='license_validate'),
url(r'v1/trending', views.listtrending, name='listtrending'),
url(r'v1/getdocument/(?P<pid>\d+)', views.getdocument, name='getdocument'),
url(r'v1/getsample/(?P<pid>\d+)', views.getsample, name='getsample'),
url(r'v1/getpromo', views.getpromo, name='getpromo'),
url(r'v1/sync', views.sync, name='sync'),
url(r'v1/voucher/gift', views.vouchergift, name='vouchergift'),
url(r'v1/voucher/pay', views.voucherpay, name='voucherpay'),
url(r'v1/voucher/redeem', views.voucherredeem, name='voucherredeem'),
url(r'v1/voucher/wallet', views.voucherwallet, name='voucherwallet'),
]
