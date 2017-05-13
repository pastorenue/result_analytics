__author__ = 'admin'

from django.conf.urls import url, patterns
from notification.views import contact

urlpatterns = patterns('',
        url(r'^$', contact, name="photobox_contact"),

       )