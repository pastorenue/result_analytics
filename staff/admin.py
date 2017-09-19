from django.contrib import admin
from .models import *

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'specialty',)
    list_display_links = ('full_name',)
