﻿# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from timerecords.models import Project, Record
from django.template import RequestContext
from django.utils import timezone
from django.contrib import auth
from django.http import HttpResponseRedirect
import datetime

def home(request):
    user=request.user
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect("/")    