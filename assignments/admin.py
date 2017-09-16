from django.contrib import admin
from .models import Assignment

class AssignmentAdmin(admin.ModelAdmin):

	class Meta:
		list_display = ('lecturer', 'question')

admin.site.register(Assignment, AssignmentAdmin)
