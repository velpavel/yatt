from timerecords.models import Project, Record
from django.utils import timezone


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

    #Возвращает множество словарей типа [{'project': project, 'level': уровень иерархии},]
def hier_childs(head_projects, user=None):
    hier_projects_list=[]
    #Иерархическая обработка
    temp=[]
    for project in head_projects:
        temp.append({'project': project, 'level': 1})
    while temp:
        k=temp[0]
        hier_projects_list.append(k)
        child_list=[]
        if user:
            all_child=k['project'].project_set.all().filter(user=user)
        else:
            all_child=k['project'].project_set.all()
        for child in all_child:
            child_list.append({'project': child, 'level': k['level']+1})
            # проверка на зацикленность
            if child in head_projects:
                return []
        temp[0:1]=child_list
    return hier_projects_list

# Расчёт длительности проекта
def prj_duration(project):
    dur=0
    for rec in Record.objects.filter(project=project):
        if rec.duration: 
            dur+=rec.duration
        else:
            a=timezone.now()-rec.start_time
            dur+=a.days*24*60*60+a.seconds
    return dur

# Расчёт длительности с учётом всех детей.
def total_duration(project):
    t_dur=0
    t_dur+=prj_duration(project)
    for child in project.project_set.all():
        t_dur+=total_duration(child)
    return t_dur