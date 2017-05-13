from django.contrib import admin
from students.models import *

class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__','reg_number','level','department')

admin.site.register(Student, StudentAdmin)
admin.site.register(Document)
admin.site.register(Project)
admin.site.register(Scholarship)

# Register your models here.
