from django.contrib import admin
from .models import StaffSetup, StudentSetup, Activation


class StaffSetupAdmin(admin.ModelAdmin):
	list_display = ('__str__',)

class StudentSetupAdmin(admin.ModelAdmin):
	list_display = ('__str__',)

class ActivationAdmin(admin.ModelAdmin):
	list_display = ('__str__',)

admin.site.register(StaffSetup, StaffSetupAdmin)
admin.site.register(StudentSetup, StudentSetupAdmin)
admin.site.register(Activation, ActivationAdmin)

# Register your models here.
