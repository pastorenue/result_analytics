from .views import setup, activate, update_quote, check_user
from django.conf.urls import patterns, url


urlpatterns = patterns('', 
	url(r'^setup/$', setup, name='user-settings'),
	url(r'^activate/$', activate, name='activate'),
	url(r'^update_quote/$', update_quote, name='update_quote'),
	url(r'^check/$', check_user, name='check_user'),

)