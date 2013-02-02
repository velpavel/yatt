﻿# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from timerecords.models import Project, Record
from django.template import RequestContext
from django.utils import timezone
import datetime

#Процедура для преобразования длительности в секундах в строку
def format_duration(duration):
    s=''
    days=duration//(24*60*60)
    if days:
        s=s+'Дней: '+str(days)+'. '
        duration=duration-(days*24*60*60)
    hours=duration//(60*60)
    if hours:
        s=s+'Часов: '+str(hours)+'. '
        duration=duration-(hours*60*60)
    minutes=duration//60
    if minutes:
        s=s+'Минут: '+str(minutes)+'. '
        duration=duration-(minutes*60)
    seconds=duration//1
    if seconds:
        s=s+'Секунд: '+str(seconds)+'.'
    return s

def project_list(request):
    #Добыча списка корневых проектов.
    projects=Project.objects.filter(user=request.user)
    #Добыча записей с нулл длительностью. и передача в форму.    
    null_rec_list=Record.objects.filter(user=request.user, duration=None)
   #Вычислим длительность для каждого проекта
    projects_list=[]
    for project in projects:
        duration=0
        recs_list=Record.objects.filter(project=project)
        for rec in recs_list:
            if rec.duration: 
                duration=duration+rec.duration
        duration=format_duration(duration)
        projects_list.append({'project': project, 'duration':duration})
    return render_to_response('timerecords/Projects_to_start.html', {'list': projects_list, 'now_going': null_rec_list}, 
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