from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
	url(r'^new-faculty$', create_faculty, name='create_faculty'),
	url(r'^new-department$', create_department, name='create_department'),
)