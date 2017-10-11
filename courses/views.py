from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from courses.models import Course
from courses.forms import CourseForm, CourseCreationForm, CourseRegistrationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from institutions.models import Department
from staff.models import Lecturer
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class CourseListView(ListView):
    model = Course
    template_name = 'courses/all.html'
    paginated_by = settings.PAGE_SIZE

    def get_queryset(self):
        queryset = Course.objects.filter(added_by=self.request.user)

        params = self.request.GET
        level = params.get('level')
        department = params.get('department')

        if level !="all" and level is not None:
            queryset = queryset.filter(level=level)
        if department != "all" and department is not None:
            queryset = queryset.filter(department_id=department)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginated_by)

        page = self.request.GET.get('page')

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        context['courses'] = queryset
        return context

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
        lecturers = params.getlist('lecturer', '')
        department = Department.objects.get(pk=dept_id)
        try:
            pay_load = {
                'course_code': course_code,
                'name': name,
                'unit': unit,
                'department': department,
                'level': level,
                'semester': semester,
            }
            course = Course(**pay_load)
            course.added_by = request.user
            course.save()
            for i in lecturers:
                lecturer = Lecturer.objects.get(pk=int(i))
                course.lecturers.add(lecturer)
            course.save()
            import pdb
            pdb.set_trace()
            messages.success(request, "The course: '%s: %s', has been successfully created" %(course.course_code, course.name))
        except Exception as e:
            messages.error(request, e)
    return HttpResponseRedirect(reverse('courses:course-list'))


def reg_course(request):
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CourseRegistrationForm()
    return render(request, 'courses/reg_course.html', {'form': form,})

@login_required
def edit_course(request, course_id):
    template_name = 'courses/edit_course.html'
    course = Course.objects.get(pk=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "The course '%s' was successfully updated" % (course))
            return HttpResponseRedirect(reverse('courses:course-list'))
    else:
        form = CourseForm(instance=course)
    return render(request, template_name, {'form': list(form), 'course': course})
