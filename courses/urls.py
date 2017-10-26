from django.conf.urls import patterns, url
from .views import new_course, reg_course, CourseListView, edit_course, RegisteredCourseView

urlpatterns = patterns('',
    url(r'^create_course/$', new_course, name='create_course'),
    url(r'^edit/(?P<course_id>\d+)/$', edit_course, name='edit'),
    url(r'^reg/$', reg_course, name='reg_course'),
    url(r'^registered/$', RegisteredCourseView.as_view(), name='course-registered'),
    url(r'^list$', CourseListView.as_view(), name='course-list')
)
