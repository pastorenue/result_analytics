from django.conf.urls import patterns, url
from .views import forum_index, post, new_response, new_category, new_reply

urlpatterns = patterns('',
	url(r'^(?P<student_slug>[\w-]+)/$', forum_index, name='forum'),
	url(r'^discussion/(?P<post_id>\d+)/$', post, name='post'),
	url(r'^response/(\d+)/$', new_response, name='response'),
	url(r'^reply/(\d+)/(\d+)/$', new_reply, name='reply'),
	url(r'^category/$', new_category, name='category'),
)