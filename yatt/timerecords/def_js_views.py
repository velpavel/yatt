# Предполагаю, что это будет вынесено в js
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from timerecords.models import Project
from django.contrib.auth.decorators import login_required

@login_required
def focus(request, prj_id=None):
    try:
        project=Project.objects.filter(user=request.user).get(pk=prj_id)
    except Exception:
        project=None
    if project:
        request.session["focus_project"] = project.id
    return HttpResponseRedirect("/tracking/")
    
@login_required
def unfocus(request):
    if 'focus_project' in request.session:
        del request.session["focus_project"]
    return HttpResponseRedirect("/tracking/")