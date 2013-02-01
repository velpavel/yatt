# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from timerecords.models import Project, Record
from django.template import RequestContext
from django.utils import timezone
import datetime

def home(request):
    user=request.user
    return render_to_response('home.html', {'user': user}) 