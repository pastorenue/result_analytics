from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from courses.models import Course
from .forms import *
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
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


class RegisteredCourseView(ListView):
    model = CourseRegistration
    template_name = 'courses/registered_courses.html'
    context_object_name = 'reg_courses'
    paginated_by = settings.PAGE_SIZE

    def get_queryset(self):
        queryset = CourseRegistration.objects.filter(student=self.request.user.student).order_by('level', 'semester')
        params = self.request.GET
        level = params.get('level', 'all')
        semester = params.get('semester', 'all')

        if level != 'all':
            queryset = queryset.filter(level=level)
        if semester != 'all':
            queryset = queryset.filter(semester=semester)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RegisteredCourseView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginated_by)

        page = self.request.GET.get('page')

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        context['reg_courses'] = queryset
        return context
        

@transaction.atomic
@login_required
@user_passes_test(lambda u: hasattr(u, 'lecturer') and u.lecturer.is_admin, login_url='/login/')
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

@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@transaction.atomic
def reg_course(request):
    extra = 1
    CourseRegFormset = formset_factory(BatchCourseForm, extra=extra)
    if request.method == 'POST':
        batch_formset = CourseRegFormset(request.POST)
        static_form = CourseRegistrationForm(request.POST)
        if static_form.is_valid() and batch_formset.is_valid():
            try:
                existing = 0
                saved = 0
                for form in batch_formset:
                    course = form.save(commit=False)
                    course.student = request.user.student
                    course.level = static_form.cleaned_data['level']
                    course.department = request.user.student.department
                    if CourseRegistration.objects.filter(course=course.course, student=course.student, session=course.session).exists() and not course.carried_over:
                        existing += 1
                    else:
                        course.save()
                        saved += 1
                messages.success(request, "You successfully registered %s courses.\
                                 %s failed because they already exist" % (saved, existing))
                return HttpResponseRedirect(reverse('courses:reg_course'))
            except Exception as e:
                messages.error(request, e)
    else:
        batch_formset = CourseRegFormset()
        static_form = CourseRegistrationForm()
    context = {
            'static_form': static_form,
            'batch_formset': batch_formset
        }

    return render(request, 'courses/reg_course.html', context)

@login_required
@user_passes_test(lambda u: hasattr(u, 'lecturer') and u.lecturer.is_admin, login_url='/login/')
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
