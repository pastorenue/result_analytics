from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import *
from django.contrib import messages
from django.db import transaction

# Create your views here.
@transaction.atomic
def create_faculty(request):
	if request.method == 'POST':
		params = request.POST
		code = params.get('code')
		name = params.get('name')

		payload = {
			'code': code,
			'name': name,
		}
		try:
			faculty = Faculty(**payload)
			faculty.save()
			messages.success(request, "'%s' has been saved" % (faculty.name))
		except Exception as e:
			messages.error(request, e)
	return HttpResponseRedirect(reverse('dashboard'))


@transaction.atomic
def create_department(request):
	if request.method == 'POST':
		params = request.POST
		code = params.get('code')
		name = params.get('name')
		faculty_id = params.get('faculty')
		faculty = Faculty.objects.get(pk=faculty_id)

		payload = {
			'code': code,
			'name': name,
			'faculty': faculty,
		}
		try:
			department = Department(**payload)
			department.save()
			messages.success(request, "'%s' has been saved" % (department.name))
		except Exception as e:
			messages.error(request, e)
	return HttpResponseRedirect(reverse('dashboard'))
