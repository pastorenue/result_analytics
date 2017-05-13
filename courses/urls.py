from django.conf.urls import patterns, url
from .views import new_course, reg_course

urlpatterns = patterns('',
    url(r'^create_course/$', new_course, name='create_course'),
    url(r'^reg/$', reg_course, name='reg_course'),
)
