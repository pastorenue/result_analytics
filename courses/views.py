from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from courses.models import Course
from courses.forms import CourseForm, CourseCreationForm, CourseRegistrationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from institutions.models import Department


@transaction.atomic
@login_required
def new_course(request):
    if request.method == 'POST':
        params = request.POST
        course_code = params.get('course_code', '')
        name = params.get('name', '')
        unit = params.get('unit', '')
        dept_id = params.get('department', '')
        semester = params.get('semester', '')
        level = params.get('level', '')
        department = Department.objects.get(pk=dept_id)

        pay_load = {
            'course_code': course_code,
            'name': name,
            'unit': unit,
            'department': department,
            'level': level,
            'semester': semester
        }
        try:
            course = Course(**pay_load)
            course.added_by = request.user
            course.save()
            messages.success(request, "The course: '%s: %s', has been successfully created" %(course.course_code, course.name))
        except Exception as e:
            messages.error(request, e)
    return HttpResponseRedirect(reverse('dashboard'))


def reg_course(request):
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CourseRegistrationForm()
    return render(request, 'courses/reg_course.html', {'form': form,})
