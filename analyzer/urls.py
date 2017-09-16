from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^plots/(?P<student_slug>[\w-]+)$', student_analysis, name='all_results_plot'),
    url(r'^cgpa/(?P<student_slug>[\w-]+)/analysis/$', student_cgpa_analysis, name='cgpa_analysis'),
    url(r'^filtered/(?P<student_slug>[\w-]+)/$', filter_data, name='filtered_plot'),
    url(r'^by_level/(?P<student_slug>[\w-]+)$', cgpa_by_level, name='cgpa_by_level'),
    url(r'^$', analytics_main, name='main_analysis_page'),
    url(r'^analsis/course/(?P<student_slug>[\w-]+)/$', course_analysis, name='course_analysis'),
    url(r'^all/$', all_analysis, name='all_analysis'),
    url(r'^predict/(?P<student_slug>[\w-]+)/$', prediction, name='prediction'),
    url(r'^predict/result/(?P<student_slug>[\w-]+)/$', make_prediction, name='make_prediction'),
    url(r'^excel/$', export_excel, name='export_excel'),
    url(r'^workspace/$', workspace, name='workspace'),
)