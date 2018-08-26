# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader
from django.db.models import *
from api.models import *
# Create your views here.
data={}
def index(request):
    template = loader.get_template('manager_dashboard.html')
    data['view'] = "dashboard"
    context = {
            'data': data
        }
    return HttpResponse(template.render(context, request))