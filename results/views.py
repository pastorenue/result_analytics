from django.shortcuts import render, render_to_response
from django.views.generic import ListView
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.db.models import Count, Sum, Aggregate
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from students.models import Student
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
import logging
import os
import csv
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from .utils import Computation, import_result_from_csv, update_results
from result_analytics.utils.excel import ExcelReport
from .models import Result, CGPA, Grading
from .forms import BatchGradingForm, GradingForm
from courses.models import Course
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from institutions.models import Department, Institution
from staff.utils import user_is_staff
from django.conf import settings


logger = logging.getLogger(__name__)

class StaffBasedResultView(ListView):
    model = Result
    template_name = 'results/staff_result_list.html'
    paginated_by = settings.PAGE_SIZE

    def get_queryset(self, **kwargs):
        queryset = Result.objects.get_staff_results(self.request)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StaffBasedResultView, self).get_context_data(**kwargs)
        results = self.get_queryset()
        paginator = Paginator(results, self.paginated_by)

        page = self.request.GET.get('page')

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results  = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        context['results'] = results
        return context

@login_required
@user_passes_test(user_is_staff, login_url='/login/')
def add_result(request):
    data = {}
    if request.method == 'POST':
        reg_number = request.POST.get("reg_number")
        course_code = request.POST.get("course")
        level = request.POST.get("level")
        score = request.POST.get("score")
        semester = request.POST.get("semester")
        session = request.POST.get("session")

        student = Student.objects.get(reg_number=reg_number)
        course = Course.objects.get(course_code=course_code)

        result_data = {
            "student": student,
            "course": course,
            "level": level,
            "exam_score": float(score),
            "semester": semester,
            "session": session,
        }
        record = Result.objects.filter(student=student, level=level, course=course, semester=semester)
        if record.exists():
            record = record[0]
            if record.exam_score != 0.0:
                messages.error(request, _(u'This result is already in the database!'))
            else:
                record.exam_score = float(score)
                record.save()
                messages.success(request, _(u'The result was successfully updated!'))
        else:
            try:
                import pdb
                pdb.set_trace()
                result = Result(**result_data)
                result.institution = request.user.lecturer.institution
                result.save()
                messages.success(request, _(u'The result for %s, was successfully Entered!') % (student))
            except Exception as e:
                messages.error(request, "It appears your school have not set a \
                    grading scheme yet. Please contact admin for help or chat a Grade-X expert now.")
        django_message = []
        for message in messages.get_messages(request):
            django_message.append(message.message)
        data['messages'] = django_message
    else:
       pass
    return TemplateResponse(request, 'results/add_results.html', {'data': data, 'courses': Course.objects.filter(lecturers__id=request.user.lecturer.id)})
# Create your views here.

@user_passes_test(user_is_staff, login_url="/login/") 
@login_required
def result_list(request):
    template_name = 'results/_results.html'
    paginated_by = settings.PAGE_SIZE
    
    results = Result.objects.filter(institution=request.user.lecturer.institution).order_by('-date_created')
    paginator = Paginator(results, paginated_by)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    
    return render(request, template_name, {'results': results})

@login_required
def result_by_student(request, student_slug):
    
    student = get_object_or_404(Student, slug=student_slug)
    results = Result.objects.filter(student_id=student.id).order_by('level')
    paginated_by = settings.PAGE_SIZE
    
    paginator = Paginator(results, paginated_by)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
        
    return render(request, 'results/personal_result.html', {'results': results, 'student': student})


def compute_cgpa(request):
    
    data = Result.objects.all().aggregate(cgpa = Sum('course_load')/Sum('credit_load'))['cgpa'] or 0
    return render(request, 'results/cgpa.html', {'data': data})


def full_detail(request, student_slug):

    return render(request, 'results/detail_result.html', {'student_id': student_id})

@login_required
def overall_result(request, student_slug):
    student = get_object_or_404(Student, slug=student_slug)
    existing_levels = []
    for rs in Result.objects.filter(student_id=student.id):
        if rs.level in existing_levels:
            pass
        else:
            existing_levels.append(rs.level)
    existing_levels.sort()

    context = {}
    levels = range(100, 600, 100)
    for level in levels:
        results = Result.objects.filter(student_id=student.id, level=level).order_by('level')
        value = 'lvl%s' % level
        context[value] = results
    context['student'] = student
    context['levels'] = existing_levels

    return render(request, 'results/overall_results.html', context)

@login_required
@user_passes_test(user_is_staff, login_url="/login/") 
def import_data(request):
    form = ImportForm()
    return render_to_response('results/result_import.html',{'form': form}, context_instance=RequestContext(request),)


def import_student(request):
    pass


@login_required
def export_excel(request):
    results = None
    institution = request.user.lecturer.institution
    if request.user.lecturer.is_admin:
        results = Result.objects.filter(institution=institution).order_by('level')
    else:
        results = Result.objects.filter(institution=institution, course__lecturers=request.user.lecturer)
    data = (("%s %s" %(e.student.first_name, e.student.last_name), e.level, e.course.name, e.total_score,e.credit_load, e.course_load, e.grade.caption)
        for e in results)
    fields = ["student", "level", "course", "total_score", "credit_load", "course_load", "grade"]
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=result.xls"
    report = ExcelReport(data, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response


 
@login_required
@user_passes_test(user_is_staff, login_url="/login/")   
def upload_csv(request):
    if request.method == 'GET':
        return render(request, 'results/_results.html', {})
    try:
        csv_file = request.FILES["file"]
        print(csv_file)
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("results:result_import"))

        # If the file is too large
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("results:result_import"))

        # else continue
        response = import_result_from_csv(csv_file, request.user.lecturer)
        if response > 0:
            messages.success(request, "Your records were successfully imported.\r\n Total Records: %s" % (response))
        else:
            messages.info(request, "It appears you do not have any new records to import.\r\n Total Records: %s" % (response))
    except Exception as e:
        messages.error(request, e)
    return HttpResponseRedirect(reverse("results:students_results"))   

@login_required
@transaction.atomic
def grading_setting(request):
    initial_data = Grading.objects.filter(institution=request.user.lecturer.institution)
    extra=0
    if len(initial_data) > 0:
        extra = 0
    else:
        extra = 1
    GradingFormset = modelformset_factory(Grading, form=BatchGradingForm, extra=extra)
    if request.method == "POST":
        params = request.POST
        institution_id = params.get('institution', '')
        if institution_id != '':
            institution = get_object_or_404(Institution, pk=institution_id)
            batch_grading_formset = GradingFormset(request.POST, queryset=initial_data)

            if batch_grading_formset.is_valid():
                try: 
                    for grade in batch_grading_formset:
                        grade = grade.save(commit=False)
                        grade.institution = institution
                        grade.save()
                    update_results(institution)
                    messages.success(request, "Your grading scheme has been saved successfully and \
                                                all existing results in the database has been modified accordingly.")
                    return HttpResponseRedirect(reverse('dashboard'))
                except IntegrityError:
                    messages.error(request, "There was an error saving your grading scheme. Please try and again or contact the Grade-X Team")
                    return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.info(request, "Sorry, You need to register an institution to set a grading scheme")
            return HttpResponseRedirect(reverse('user_index'))
    else:
        gradingform = GradingForm()
        batch_grading_formset = GradingFormset(queryset=initial_data)

    context = {
        'grading_form': gradingform,
        'batch_grading_formset': batch_grading_formset
    }

    return render(request, 'results/grading_settings.html', context)


