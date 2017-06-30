"""result_analytics URL Configuration
"""

from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from result_analytics.views import index, home, register_user, register_success
from django.views.static import serve

urlpatterns = [ 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^students/', include('students.urls', namespace='students')),
    url(r'^$', index, name='user_index'),
    url(r'^results/', include('results.urls', namespace='results')),
    url(r'^analytics/', include('analyzer.urls', namespace='analyzer')),
    url(r'^staff/', include('staff.urls')),
]
    
urlpatterns+=patterns('django.contrib.auth.views',
        url(r'^login/$', 'login', {'template_name': 'login.html'}, name='result_login'),
        url(r'^password-reset/$', 'password_reset', {
            'template_name': 'password_reset.html',
            'email_template_name': 'password_reset_email.html',
            'subject_template_name':'password_reset_subject.txt',
            'post_reset_redirect': ('result_reset_done'),
            'html_email_template_name':'password_reset_email.html',
            }, name="result_password_reset"),
        url(r'^password-reset-done/$', 'password_reset_done', {'template_name':'password_reset_done.html',}, name="result_reset_done"),
        url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'password_reset_confirm',{'template_name':'password_reset_confirm.html',}, name="photobox_reset_confirm"),
        url(r'^password-reset-complete/$', 'password_reset_complete',{'template_name':'password_reset_complete.html',}, name="result_reset_complete"), 
        url(r'^logout/$', 'logout', {'next_page': 'result_login'}, name="result_logout"),
)

urlpatterns+=patterns('',
        url(r'^successful/$', register_success, name="result_success"),
         url(r'^signup/$', register_user, name="result_signup"),
)

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


