from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from result_analytics.utils.excel import ExcelReport
from .models import Student, UniqueMapper
from django.db import transaction
from courses.models import *
from students.models import Student
from results.models import Result


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


def user_is_student(user):
    return Student.objects.filter(user=user).exists() 


@transaction.atomic
def generate_mapper_excel(excel_file):
    from xlrd import open_workbook
    from openpyxl import load_workbook
    from xlutils.copy import copy
    import xlwt
    import urllib
    
    read_book = open_workbook(file_contents=excel_file.read())
    work_book = copy(read_book)
    sheet = read_book.sheet_by_index(0)
    new_sheet = work_book.get_sheet(0)
    headers = ['REG NUMBER', 'SHORT INSTITUTION CODE', 'REG MAPPER']
    mapper_column = []
    style1 = xlwt.easyxf('pattern: pattern solid, fore_colour red;')

    for row in range(1, sheet.nrows):
        reg_number = sheet.cell(row, 0).value
        short_institution_name = sheet.cell(row, 1).value
        mapper = UniqueMapper(reg_number=reg_number, short_institution_name=short_institution_name)
        mapper.save()
        mapper_column.append(mapper.unique_map)

    for row in range(len(mapper_column)):
        if row == len(mapper_column):
            break
        else:
            new_sheet.write(row+1, 2, mapper_column[row])
    for col in range(len(headers)):
        new_sheet.write(0,col, headers[col], style1)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "inline; filename=%s.xls" % (excel_file.name[:-3])

    work_book.save(response)
    return response

def has_completed_level(student):
    results = Result.objects.filter(student=student, level=student.level)
    reg_courses = CourseRegistration.objects.filter(student=student, level=student.level)

    set_result = set(results)
    set_registration = set(reg_courses)

    set_differences = set_registration.difference(set_result)
    if len(set_differences) > 0:
        return False
    return False