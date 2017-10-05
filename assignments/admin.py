from django.contrib import admin
from .models import Assignment, AssignmentScore

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

	class Meta:
		list_display = ('lecturer', 'question')

@admin.register(AssignmentScore)
class AssignmentScoreAdmin(admin.ModelAdmin):

	class Meta:
		list_display = ('student', 'assignment', 'score')
