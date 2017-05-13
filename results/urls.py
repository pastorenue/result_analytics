from django.conf.urls import patterns, url
from .views import add_result, compute_cgpa, result_list,\
    result_by_student, import_data, export_excel, full_detail, overall_result

urlpatterns = patterns('',
    url(r'^add_results/$', add_result, name='add_result'),
    url(r'^import_data/$', import_data, name='result_import'),
    url(r'^cgpa/student_cgpa/$', compute_cgpa, name='compute_cgpa'),
    url(r'^$', result_list, name='students_results'),
    url(r'^$', result_list, name='students_results'),
    url(r'^own_results/(?P<student_id>\d+)/$', result_by_student, name='personal_results'),
    url(r'^overall_results/(?P<student_id>\d+)/$', overall_result, name='all_results'),
    url(r'^(?P<student_id>\d+)/result_details/$', full_detail, name='full_detail'),
    url(r'^excel/$', export_excel, name='export_excel'),
)