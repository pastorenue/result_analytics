from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('', 
	url(r'^list/$', ProjectListView.as_view(), name='my_projects'),
	url(r'^supervision-list/$', StaffProjectListView.as_view(), name='supervision'),
	url(r'^details/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', ProjectDetailView.as_view(), name='project_detail'),
	url(r'^edit-project/(?P<project_id>\d+)/$', update_project, name='edit-project'),
	url(r'^add/$', new_project, name='new_project'),
)