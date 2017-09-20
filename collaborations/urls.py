from django.conf.urls import patterns, url
from friendship.models import Follow, Friend
from .views import *

urlpatterns = patterns("",
	url(r'^friend_list/$', collaboration_index, name='collaboration_index'),
	url(r'^friend_zone/$', friend_zone, name='friend-zone'),
	url(r'^send_request/$', send_request, name='add-friend'),
	url(r'^accept/(?P<friend_request_id>\d+)/$', accept_request, name='accept'),
	url(r'^reject/(?P<friend_request_id>\d+)/$', reject_request, name='reject'),
	url(r'^follow/(?P<to_user_id>\d+)/$', follow, name='follow'),
	url(r'^cancel/(?P<to_user_id>\d+)/$', cancel_friendship, name='cancel_friendship'),
	url(r'^mark$', mark_all_as_read, name='mark'),
)