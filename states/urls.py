from django.conf.urls import patterns, url
from states.models import Country, State, LGA

urlpatterns = patterns('states.views',
    url(r'^state/find-by-country/$', 'filter', {'model_class': State, 'field_name': 'country__pk'}, name='states_state_by_country'),
    url(r'^lga/find-by-state/$', 'filter', {'model_class': LGA, 'field_name': 'state__pk'}, name='states_lga_by_state'),
)
