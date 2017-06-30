from django.shortcuts import render, render_to_response
from django.views.generic import ListView
from django.forms.formsets import formset_factory
from django.db.models import Count, Sum, Aggregate
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
from .models import Result, CGPA
from courses.models import Course
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from institutions.models import Department


logger = logging.getLogger(__name__)

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
        course = Course.objects.get(course_code=str(course_code).upper())

        result_data = {
            "student": student,
            "course": course,
            "level": level,
            "score": float(score),
            "semester": semester,
            "session": session,
        }
        num_exist = Result.objects.filter(student=student, level=level, course=course, semester=semester).count()
        if num_exist>0:
            messages.error(request, _(u'This result is already in the database!'))
        else:
            result = Result(**result_data)
            result.save()
            messages.success(request, _(u'The result was entered successfully!'))
        django_message = []
        for message in messages.get_messages(request):
            django_message.append(message.message)
        data['messages'] = django_message
    else:
       pass
    return TemplateResponse(request, 'results/add_results.html', {'data': data})
# Create your views here.

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


def result_by_student(request, student_id):
    
    student = get_object_or_404(Student, pk=student_id)
    results = Result.objects.filter(student_id=student_id).order_by('level')
    
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


def full_detail(request, student_id):

    return render(request, 'results/detail_result.html', {'student_id': student_id})


def overall_result(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    existing_levels = []
    for rs in Result.objects.filter(student_id=student_id):
        if rs.level in existing_levels:
            pass
        else:
            existing_levels.append(rs.level)
    existing_levels.sort()

    context = {}
    levels = range(100, 600, 100)
    for level in levels:
        results = Result.objects.filter(student_id=student_id, level=level).order_by('level')
        value = 'lvl%s' % level
        context[value] = results
    context['student'] = student
    context['levels'] = existing_levels

    return render(request, 'results/overall_results.html', context)


def import_data(request):
    form = ResultImportForm()
    return render_to_response('results/result_import.html',{'form': form}, context_instance=RequestContext(request),)


def import_student(request):
    pass

def export_excel(request):
    results = (("%s %s" %(e.student.first_name, e.student.last_name), e.level, e.course.name, e.score,e.credit_load, e.course_load, e.grade.caption)
        for e in Result.objects.order_by('level'))
    fields = ["student", "level", "course", "score", "credit_load", "course_load", "grade"]
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=result.xls"
    report = ExcelReport(results, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response
    
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