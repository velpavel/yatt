# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from timerecords.models import Project, Record
from timerecords.forms import RecordForm, ProjectForm
from timerecords.def_modules import format_duration, hier_childs
from django.utils import timezone
import datetime

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
    hier_projects_list=hier_childs(head_projects=projects, user=request.user)
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
    if request.method == 'POST':
        form=RecordForm(request.POST, instance=rec)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tracking/%s/' %rec.project.id)
    else:
        form=RecordForm(instance=rec)
    return render_to_response('timerecords/edit_rec.html', {'rec': rec, 'form': form,}, context_instance=RequestContext(request))
    
# Редактирование проекта. Возникает ошибка, если редкатрировать проект, которые замкнут в иерархическю петлю
def edit_project(request, prj_id=None):
    try:
        project=Project.objects.filter(user=request.user).get(pk=prj_id)
    except Exception:
        project=None
#Получаем список проектов. которые не могут быть родителями
    child_list=hier_childs(head_projects=[project,], user=request.user)
    if not child_list:
        #Тут надо совсем опечалиться и что-то нибудь умное сделать. Например:
        project.parent=None
        project.save()
        child_list=hier_childs(head_projects=[project,], user=request.user)
    can_not_be_parrent = []
    for pr in child_list:
        can_not_be_parrent.append(pr['project'].id)
    can_be_parent=Project.objects.filter(user=request.user).exclude(pk__in=can_not_be_parrent)
    id_can_be_parent=[]
    for pr in can_be_parent:
        id_can_be_parent.append(pr.id)
#Приступаем к дальнейшей обработке
    if request.method == 'POST':
        form=ProjectForm(id_can_be_parent, request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tracking/%s/' %project.id)
    else:
        form=ProjectForm(id_can_be_parent, instance=project)
    return render_to_response('timerecords/edit_rec.html', {'rec': project, 'form': form,}, context_instance=RequestContext(request))