from django.conf.urls import patterns, url
from .views import accounts, StaffAnalyticsView, chart_data_json, other_uploads

urlpatterns = patterns('',
   url(r'^accounts/$', accounts, name='staff_account'),
   url(r'^analytics/$', StaffAnalyticsView.as_view(), name='staff_analytics'),
   url(r'^charts/json/$', chart_data_json, name='chart_data_json'),
   url(r'^import/json/$', other_uploads, name='import_json'),
)