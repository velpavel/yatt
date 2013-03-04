# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from timerecords.models import Project, Record
from django.template import RequestContext
from django.utils import timezone
from django.contrib import auth
from django.http import HttpResponseRedirect
from yatt.forms import UserCreationForm
import datetime

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect("/")
    
def registr(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.email=new_user.username
            new_user.save()
            new_user.backend='django.contrib.auth.backends.ModelBackend'
            auth.login(request, new_user)
            return HttpResponseRedirect('/')
    else:
        form=UserCreationForm()
    return render_to_response("registration/register.html", {'form': form,}, context_instance=RequestContext(request))
    
    return render_to_response('home.html', {}, context_instance=RequestContext(request))