from timerecords.models import Project


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
def hier_childs(head_projects, user):
    hier_projects_list=[]
    #Иерархическая обработка
    temp=[]
    for project in head_projects:
        temp.append({'project': project, 'level': 1})
    while temp:
        k=temp[0]
        hier_projects_list.append(k)
        child_list=[]
        for child in k['project'].project_set.all().filter(user=user):
            child_list.append({'project': child, 'level': k['level']+1})
            # проверка на зацикленность
            if child in head_projects:
                return []
        temp[0:1]=child_list
    return hier_projects_list