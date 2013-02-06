# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from timerecords.models import Project, Record
from timerecords.forms import RecordForm
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
    if seconds or not s:
        s=s+'Секунд: '+str(seconds)+'.'
    return s

def project_list(request):
    #Добыча записей с нулл длительностью
    null_rec_list=Record.objects.filter(user=request.user, duration=None)
    #Обработка старта/остановки треккинга
    if 'prjct' in request.POST:
        #! После тестов вставить сюда из start
        #Обновление списка записей с нулл длительностью.    
        null_rec_list=Record.objects.filter(user=request.user, duration=None)
    
    #Добыча списка корневых проектов. 
    #Если нет чётких корневых, будем использовать просто список проектов.
    projects=Project.objects.filter(user=request.user, parent=None)
    hier_projects_list=[]
    #Иерархическая обработка
    temp=[]
    for project in projects:
        temp.append({'project': project, 'level': 1})
    while temp:
        k=temp[0]
        hier_projects_list.append(k)
        child_list=[]
        for child in k['project'].project_set.all().filter(user=request.user):
            child_list.append({'project': child, 'level': k['level']+1})
        temp[0:1]=child_list
    #Здесь начнём обработку проетов без корневого
    projects=Project.objects.filter(user=request.user)
    now_we_have_projects=[]
    for project in hier_projects_list:
        now_we_have_projects.append(project['project'])
    #добавим уровень иерархии 0
    for project in projects:
        if project not in now_we_have_projects:
            hier_projects_list.append({'project': project, 'level': 0})   
   
   #Вычислим длительность для каждого проекта
    projects_list=[]
    for project in hier_projects_list:
        duration=0
        recs_list=Record.objects.filter(project=project['project'])
        for rec in recs_list:
            if rec.duration: 
                duration=duration+rec.duration
        duration=format_duration(duration)
        #Текущий символ обозначения иерархии
        hier='->'
        projects_list.append({'project': project['project'], 'level': hier*project['level'], 'duration': duration})
    return render_to_response('timerecords/Projects_to_start.html', {'list': projects_list, 'now_going': null_rec_list}, 
                                context_instance=RequestContext(request)) 
                                

# Процедура старта записи.
# Вызывается только передачей данных из формы. !добавить обработку ошибок. если не из формы. И включить в проджект лист
# Сейчас нужна для вывода отладочной инфы
def start(request):
    #Добыча записей с нулл длительностью
    null_rec_list=Record.objects.filter(user=request.user, duration=None)
    #Обработка старта/остановки треккинга
    if 'prjct' in request.POST:
        for rec in null_rec_list:
            a=timezone.now()-rec.start_time
            rec.duration=a.days*24*60*60+a.seconds
            rec.save()
        pr_answer=request.POST['prjct']
        #Если заводим запись в новый проект:
        if pr_answer=='-2' and request.POST['newprjct']:
            pr_new=Project(user=request.user, name=request.POST['newprjct'], new=True)
            pr_new.save()
            pr_answer=pr_new.id
        #Продолжаем какой-то проект или останавливаем всё:
        else:
            try:
                pr=Project.objects.get(pk=pr_answer)
            except Exception:
                rec_new=None
            else:
                rec_new = Record(user=request.user, project=pr, start_time=timezone.now())
                rec_new.save()
    return render_to_response('timerecords/start.html', {'rec': rec_new, 'rec_list':null_rec_list})
    
def edit_record(request, rec_id=None):
    try:
        rec=Record.objects.filter(user=request.user).get(pk=rec_id)
    except Exception:
        rec=None
    form=RecordForm(instance=rec)
    return render_to_response('timerecords/edit_rec.html', {'rec': rec, 'form': form,})