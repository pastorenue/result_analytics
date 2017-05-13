from django.contrib import admin
from .models import Country, State, LGA

admin.site.register(Country)
admin.site.register(State)
admin.site.register(LGA)

# Register your models here.
