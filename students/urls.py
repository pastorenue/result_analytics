from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .forms import *
from .views import (StudentListView, student_profile, request_help, 
                    export_excel, create_student, update_photo, student_chart_json,  
                    mapper_excel_generator, generate, generate_mapper_json, 
                    edit_profile, StudentAnalyticsView)
urlpatterns = patterns('',
    url(r'^$', StudentListView.as_view(), name='students_list'),
    url(r'^analysis/$', login_required(StudentAnalyticsView.as_view()), name='student_analytics'),
    url(r'^new_student/$', create_student, name='create_student'),
    url(r'^profile/(?P<student_slug>[\w-]+)/$', student_profile , name='student_account'),
    url(r'^excel/$', export_excel, name='export_excel'),
    url(r'^mapper/$', mapper_excel_generator, name='mapper'),
    url(r'^update-profile/$', edit_profile, name='edit-profile'),
    url(r'^mapper/generator/$', generate, name='generate'),
    url(r'^update-photo/$', update_photo, name='update_photo'),
    url(r'^student-json/$', student_chart_json, name='student_chart_json'),
    url(r'^mapper-json/$', generate_mapper_json, name='mapper-json'),
    url(r'^ineed/assistance/(?P<student_id>\d+)/$', request_help , name='help'),
)