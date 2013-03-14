from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from timerecords.models import Project
from django.views.generic import ListView, DetailView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    #Главная - просто заглушка. Это временная мера
    url(r'^$', 'yatt.views.home'),
    url(r'^accounts/login/$',login),
    url(r'^accounts/logout/$','yatt.views.logout'),
    url(r'^accounts/registr/$','yatt.views.registr'),
    #когда-нибудь тут будет другая ссыль
    url(r'^accounts/profile/$', 'yatt.views.home'),
    # Список проектов с возможностью посмотреть вложенные.
    # Теперь это отдадочный список для просмотра проектов всех пользователей.
    url(r'^tracking/index/$', 
        ListView.as_view(
            queryset=Project.objects.order_by('name'),
            context_object_name='projects_list',
            template_name='timerecords/index.html')),
    # Детальный вид проекта.
    # !Изменить отображение записей - добавить длительность и суммарную длительность проекта
    url(r'^tracking/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Project,
            template_name='timerecords/project.html')),
            
    url(r'^tracking/(?P<prj_id>\d+)/new/$', 'timerecords.views.show_project'),
    # редактирование записей
    url(r'^tracking/record/(?P<rec_id>\d+)/$', 'timerecords.views.edit_record'),
    # удаление записей
    url(r'^tracking/record/(?P<rec_id>\d+)/del/$', 'timerecords.views.del_record'),
    # редактирование проектов
    url(r'^tracking/project/(?P<prj_id>\d+)/$', 'timerecords.views.edit_project'),
    # удаление проектов
    url(r'^tracking/project/(?P<prj_id>\d+)/del/$', 'timerecords.views.del_project'),
    # Выбрать новые проекты
    url(r'^tracking/new_projects/$', 'timerecords.views.show_new_projects'),
    
    # Начало записи в проекте. Потом объеденить с index?
    url(r'^tracking/$', 'timerecords.views.project_list'),
    
    #js url - потом будут засунуты в js и удалены.
    # фокус на проектк
    url(r'^tracking/project/(?P<prj_id>\d+)/focus/$', 'timerecords.def_js_views.focus'),
    # снять фокус
    url(r'^tracking/unfocus/$', 'timerecords.def_js_views.unfocus'),
    
)
