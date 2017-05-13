from django.conf.urls import patterns, url
from .views import dashboard

urlpatterns = patterns('',
    url(r'^dashboard/$', dashboard, name='staff_index'),
    #url(r'^cgpa/$', cgpa_chart_view, name=''),
)