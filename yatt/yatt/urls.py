from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from timerecords.models import Project
from django.views.generic import ListView, DetailView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yatt.views.home', name='home'),
    # url(r'^yatt/', include('yatt.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',login),
    url(r'^accounts/logout/$',logout),
    url(r'^tracking/$', 
        ListView.as_view(
            queryset=Project.objects.order_by('name'),
            context_object_name='projects_list',
            template_name='timerecords/index.html')),
    url(r'^tracking/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Project,
            template_name='timerecords/project.html')),
    url(r'^tracking/test/$', 'timerecords.views.project_list'),
    url(r'^tracking/start/$', 'timerecords.views.start'),
    
)
