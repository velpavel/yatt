# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from timerecords.models import Project, Record
from django.template import RequestContext
from django.utils import timezone
import datetime

def project_list(request):
    #Добыча списка проеrтов.
    projects_list=Project.objects.filter(user=request.user)
    #Добыча записей с нулл длительностью. и передача в форму.    
    
    #На форме остановить для запущенного и продолжить для списка.
    return render_to_response('timerecords/Projects_to_start.html', {'list': projects_list}, 
                                context_instance=RequestContext(request)) 
                                

# Процедура старта записи.
# Вызывается только передачей данных из формы. !добавить обработку ошибок. если не из формы. И вкулючить в проджект лист
# Сейчас нужна для вывода отладочной инфы
def start(request):
    pr=Project.objects.get(pk=request.POST['prjct'])
    null_rec_list=Record.objects.filter(user=request.user, duration=None)
    for rec in null_rec_list:
        a=timezone.now()-rec.start_time
        rec.duration=a.days*24*60*60+a.seconds
        rec.save()
    rec_new = Record(user=request.user, project=pr, start_time=timezone.now())
    rec_new.save()
    return render_to_response('timerecords/start.html', {'rec': rec_new, 'rec_list':null_rec_list})