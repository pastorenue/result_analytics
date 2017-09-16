from django.shortcuts import render, render_to_response
from django.views.generic import ListView
from django.forms.formsets import formset_factory
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
from .utils import Computation, import_result_from_csv
from result_analytics.utils.excel import ExcelReport
from .models import Result, CGPA, Grading
from .forms import BatchGradingForm, GradingForm
from courses.models import Course
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from institutions.models import Department, Institution
from staff.utils import user_is_staff


logger = logging.getLogger(__name__)

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
            result = Result(**result_data)
            messages.success(request, _(u'The result was successfully Entered!'))
        django_message = []
        for message in messages.get_messages(request):
            django_message.append(message.message)
        data['messages'] = django_message
    else:
       pass
    return TemplateResponse(request, 'results/add_results.html', {'data': data, 'courses': Course.objects.filter(lecturer=request.user.lecturer)})
# Create your views here.

@user_passes_test(user_is_staff, login_url="/login/") 
@login_required
def result_list(request):
    template_name = 'results/_results.html'
    
    results = Result.objects.all().order_by('-date_created')
    paginator = Paginator(results, 30)
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
    
    paginator = Paginator(results, 10)
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
    results = (("%s %s" %(e.student.first_name, e.student.last_name), e.level, e.course.name, e.score,e.credit_load, e.course_load, e.grade.caption)
        for e in Result.objects.order_by('level'))
    fields = ["student", "level", "course", "score", "credit_load", "course_load", "grade"]
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=result.xls"
    report = ExcelReport(results, fields, groupby=request.GET.get('groupby'))
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
        response = import_result_from_csv(csv_file)
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
    GradingFormset = formset_factory(BatchGradingForm)
    initial_data = {}
    if request.method == "POST":
        params = request.POST
        institution_id = params.get('institution', '')
        if institution_id != '':
            institution = get_object_or_404(Institution, pk=institution_id)
            gradingform = GradingForm(request.POST)
            batch_grading_formset = GradingFormset(request.POST)

            if gradingform.is_valid() and batch_grading_formset.is_valid():
                new_grades = []

                for grading in batch_grading_formset:
                    caption = grading.cleaned_data.get('caption')
                    grade_points = grading.cleaned_data.get('grade_points')
                    start = grading.cleaned_data.get('start')
                    end = grading.cleaned_data.get('end')

                    if caption != '' and grade_points != '' and start != '' and end != '':
                        new_grades.append(Grading(institution=institution, 
                                    caption=caption, grade_points=grade_points, 
                                    start=start, end=end))
                try: 
                    if not len(new_grades) == 0:
                        Grading.objects.bulk_create(new_grades)
                        messages.success(request, "Your grading scheme has been saved successfully")
                        return HttpResponseRedirect(reverse('dashboard'))
                    else:
                        messages.error(request, "Ooops!!, Please fill out the fields before saving")
                except IntegrityError:
                    messages.error(request, "There was an error saving your grading scheme. Please try and again or contact Acadlytics Team")
                    return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.info(request, "Sorry, You need to register an institution to set a grading scheme")
            return HttpResponseRedirect(reverse('user_index'))
    else:
        gradingform = GradingForm()
        batch_grading_formset = GradingFormset(initial=initial_data)

    context = {
        'grading_form': gradingform,
        'batch_grading_formset': batch_grading_formset
    }

    return render(request, 'results/grading_settings.html', context)


