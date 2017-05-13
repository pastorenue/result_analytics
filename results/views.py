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
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from .utils import Computation, import_result_from_csv
from result_analytics.utils.excel import ExcelReport
from .models import Result, CGPA
from institutions.models import Department

logger = logging.getLogger(__name__)

def add_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            num_exist = Result.objects.filter(student=form.cleaned_data['student'], level=form.cleaned_data['level'], course=form.cleaned_data['course'], semester=form.cleaned_data['semester']).count()
            if num_exist>0:
                messages.error(request, _(u'This result is already in the database!'))
            else:
                result = Result(**data)
                result.save()
                form = ResultForm()
                messages.success(request, _(u'The Results have been successfully entered!'))
    else:
        form = ResultForm()
    return TemplateResponse(request, 'results/add_results.html', {'form': form})
# Create your views here.

def result_list(request):
    template_name = 'results/_results.html'
    
    results = Result.objects.all().order_by('-date_created')
    paginator = Paginator(results, 15)
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
    if request.method == 'POST':
        form = ResultImportForm(request.POST, request.FILES)
        if form.is_valid():
            param_file = request.FILES['file']
            import_result_from_csv(open(os.path.expanduser('~/Desktop/Results_Uploads/%s' % param_file)))
            return render_to_response('results/result_import.html', {'form': form}, context_instance=RequestContext(request),)
            return HttpResponseRedirect(reverse('main_analysis_page'))
    else:
        form = ResultImportForm()
        if os.path.exists(os.path.expanduser('~/Desktop/Results_Uploads')):
            pass
        else:
            os.mkdir(os.path.expanduser("~/Desktop/Results_Uploads"))
    return render_to_response('results/result_import.html',{'form': form}, context_instance=RequestContext(request),)


def export_excel(request):
    results = (("%s %s" %(e.student.first_name, e.student.last_name), e.level, e.course.name, e.score,e.credit_load, e.course_load, e.grade.caption)
        for e in Result.objects.order_by('level'))
    fields = ["student", "level", "course", "score", "credit_load", "course_load", "grade"]
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=result.xls"
    report = ExcelReport(results, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response
    