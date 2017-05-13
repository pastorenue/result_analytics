from django.contrib import admin
from .models import *

class InstitutionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'location')


class InstitutionsDetailAdmin(admin.ModelAdmin):
    list_display = ('institution', 'full_address')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('faculty',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

class LecturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'specialty',)
    list_display_links = ('name',)

admin.site.register(Institution, InstitutionsAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(InstitutionDetail, InstitutionsDetailAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Position)
