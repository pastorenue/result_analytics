from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from courses.models import Course
from courses.forms import CourseForm, CourseRegistrationForm
from django.contrib import messages
from django.utils.translation import ugettext as _

@login_required
def new_course(request):
    if request.method == 'POST':
        owner = Course(added_by=request.user)
        form = CourseForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            form=CourseForm()
            messages.success(_(u'The course: %s: %s has being successfully created!' % (form.cleaned_data['code'], form.cleaned_data['name'])))
    else:
        form = CourseForm()
    return render(request, 'courses/course_create.html', {'form': form})

# Create your views here.

def reg_course(request):
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CourseRegistrationForm()
    return render(request, 'courses/reg_course.html', {'form': form,})
