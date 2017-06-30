from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from .models import Student
from institutions.models import Department, Faculty
from results.models import Result
from students.models import Student
from result_analytics.utils.excel import ExcelReport
from django.db.models import Q


class StudentListView(ListView):
    model = Student
    template_name = 'students/_list_students.html'
    context_object_name = "students"

    def get_queryset(self):
        queryset = Student.objects.all()

        department = self.request.GET.get("department", "all")
        faculty = self.request.GET.get("faculty", "all")
        student = self.request.GET.get("student", "")
        level = self.request.GET.get("level", "all")
        status = self.request.GET.get("status", "status")

        if department != "all":
            queryset = queryset.filter(department__name=department)
        if faculty != "all":
            queryset = queryset.filter(faculty__name=faculty)
        if student != "":
            queryset = queryset.filter(Q(reg_number__icontains=student) | Q(last_name__icontains=student) | Q(first_name__icontains=student))
        if level != "all":
            queryset = queryset.filter(level=level)
        if status != "status":
            queryset = queryset.filter(user_status=status)
        
        return queryset

    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StudentListView, self).get_context_data(**kwargs)
        context["departments"] = Department.objects.all()
        context["faculties"] = Faculty.objects.all()

        return context

@login_required
def student_profile(request, student_id=None):
    student = get_object_or_404(Student, pk=student_id)
    is_own_profile = (student.user == request.user)
    
    my_rank = ranking(student)
    
    documents = student.document_set.all()
    template_name = 'student_profile'
    return render(request, 'students/%s.html' % template_name, {'rank': my_rank, 'documents': documents, 'student': student, 'is_own_profile': is_own_profile})

def ranking(student):
    results = Result.objects.all()
    ranking_data = {}
    
    all_students = Student.objects.all()
    for stu in all_students:
        grade = 0
        for result in results:
            if result.student == stu:
                grade+=result.credit_load
        ranking_data[stu] = grade
    sort = sorted(ranking_data, key= ranking_data.__getitem__, reverse=True)
    
    return sort.index(student)+1

def export_excel(request):
    students = ((e.last_name, e.first_name, e.reg_number, e.level, e.sex, e.birth_date or '', e.program_type, e.department.name or '', e.faculty.name or '')
        for e in Student.objects.order_by('level'))
    fields = ["last_name", "first_name", "reg_number", "level", "sex", "birth_date", "program_type", "department", "faculty"]
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=students.xls"
    report = ExcelReport(students, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response
  

# Create your views here.


