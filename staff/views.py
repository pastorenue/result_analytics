from django.shortcuts import render
from django.db.models import * 
from results.models import Result
from institutions.models import Department, Lecturer
#from chartit import DataPool, Chart


def dashboard(request):
     template = ''
     if request.user.is_superuser:
         template = 'staff/dashboard.html'
     else:
         template = 'students/dashboard.html'
                
     context = {
         
         
     }
     return render(request, template, context)
