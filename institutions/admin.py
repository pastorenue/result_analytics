from django.contrib import admin
from .models import *

class InstitutionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'location')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('faculty',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

admin.site.register(Institution, InstitutionsAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Faculty, FacultyAdmin)
