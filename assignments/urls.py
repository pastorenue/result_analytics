from django.conf.urls import patterns, url
from .views import (deactivate, AssignmentScoreListView, 
					assignment_detail, create_assignment, 
					AssignmentView, submit_assignment, 
					score_sheet, mark)

urlpatterns = patterns("",
	url(r'^all-assignments/$', AssignmentScoreListView.as_view(), name='all_assignments'),
	url(r'^create/$', create_assignment, name='create_assignment'),
	url(r'^list/$', AssignmentView.as_view(), name='staff_assignments'),
	url(r'^details/(?P<assignment_code>[\w-]+)/$', assignment_detail, name='assignment_detail'),
	url(r'^submit/(?P<assignment_code>[\w-]+)/$', submit_assignment, name='submit_assignment'),
	url(r'^deactivate/(?P<assignment_id>\d+)/$', deactivate, name='deactivate'),
	url(r'^score-sheet/(?P<assignment_id>\d+)/$', score_sheet, name='score-sheet'),
	url(r'^marked/(?P<assignment_id>\d+)/$', mark, name='marked'),
)