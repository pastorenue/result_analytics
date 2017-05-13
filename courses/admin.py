from django.contrib import admin
from .models import *

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_code',)

class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'level' )


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseRegistration, CourseRegistrationAdmin)
