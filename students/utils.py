from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from result_analytics.utils.excel import ExcelReport
from result_analytics.utils.pdf import render_pdf


def export_performance_excel():
    all_cgpa = main.get_performance_report()
    
    students = Student.objects.all()
    print(all_cgpa)
    fcgpa = ((student.full_name, student.reg_number, all_cgpa[student]) for student in students)
    fields = ["student","reg number","FCGPA"]
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=performance_report.xls"
    report = ExcelReport(fcgpa, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response

def export_transcript_pdf():
    pass

