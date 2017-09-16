from django.contrib import admin
from .models import *

class ResultAdmin(admin.ModelAdmin):
    list_display = ('course','credit_load', 'student',  'total_score', 'grade', 'course_load')

class GradingAdmin(admin.ModelAdmin):
    list_display = ('institution', 'caption', 'start', 'end')

class AdminCGPA(admin.ModelAdmin):
    list_display = ('student','level','session','cgpa','date_created')
    #code
    

admin.site.register(Result, ResultAdmin)
admin.site.register(Grading, GradingAdmin)
admin.site.register(CGPA, AdminCGPA)
# Register your models here.
