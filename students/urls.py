from django.conf.urls import patterns, url
from .views import StudentListView, student_profile, export_excel

urlpatterns = patterns('',
    url(r'^$', StudentListView.as_view(), name='students_list'),
    url(r'^profile/(?P<student_id>\d+)/$', student_profile , name='student_profile'),
    url(r'^excel/$', export_excel, name='export_excel'),
)

