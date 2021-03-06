from django.conf.urls import patterns, url
from .views import  (
				accounts, StaffAnalyticsView, StaffListView, 
				chart_data_json, other_uploads, 
				create_staff, edit_profile)

urlpatterns = patterns('',
   url(r'^accounts/$', accounts, name='staff_account'),
   url(r'^edit-profile/$', edit_profile, name='edit-profile'),
   url(r'^list/$', StaffListView.as_view(), name='staff-list'),
   url(r'^new-staff/$', create_staff, name='new-staff'),
   url(r'^analytics/$', StaffAnalyticsView.as_view(), name='staff_analytics'),
   url(r'^charts/json/$', chart_data_json, name='chart_data_json'),
   url(r'^import/json/$', other_uploads, name='import_json'),
)