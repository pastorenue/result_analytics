from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, Aggregate
from chartit import DataPool, Chart
from students.models import Student
from staff.models import Lecturer
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import json
from result_analytics.utils.excel import ExcelReport
from results.models import Result, CGPA
from decimal import Decimal
from courses.models import Course
from analyzer.utils import cgpaData, StudentChartData, RegressionModel, ResultData, MainData as main
from results.utils import Computation as cp

@login_required
def workspace(request):
    return render(request, 'analyzer/workspace.html', {})

@login_required
def lecturer_analysis(request, staff_id):
    staff = Lecturer.objects.filter(pk=staff_id)
    
    result = Result.objects.all()
    data = []
    courses = Course.objects.all()
    
    pass

def analytics_main(request):
    template_name = "analyzer/analytics_main.html"
    
    return render(request, template_name, {})
    pass

def course_analysis(request, course_id=None, department=None, level=None):
    template_name = "analyzer/_analyze_course.html"
    
    pass

@login_required
def cgpa_by_level(request,  student_slug, chartID='container', chart_type = 'area', chart_height=300):
    student = get_object_or_404(Student, slug=student_slug)
    fcgpa = cgpaData.get_fcgpa(student.id)
    grades = cp.get_grades(student.institution)
    degree = cp.get_cgpa_comment(student.institution, fcgpa)

    cgpa = []
    level = []
    pseudo_level = []
    data = {'level':[], 'cgpa':[]}
    res = Result.objects.filter(student_id=student.id)
    for r in res:
        pseudo_level.append(r.level)
    for i in range(100, 700, 100):
        if i in pseudo_level:
            data['level'].append(i)
            data['cgpa'].append(cgpaData.get_level_cgpa(i, student.id))
    
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'xy'}
    title = {"text": "%s's CGPA Breakdown" % (student)}
    xAxis = {"title": {"text": 'Level'}, "categories": data['level']}
    yAxis = {"title": {"text": "CGPA values"}, "min": 0, "max": max(grades), "tickInterval": 0.5}
    series = [{"name": "Student CGPA", "data": data['cgpa']}]
     
    
    context = {
        'fcgpa': fcgpa,
        'max_grade': max(grades),
        'degree': degree,
        'chartID': chartID,
        'chart': chart,
        'title': title,
        'xAxis': xAxis,
        'student': student,
        'yAxis': yAxis,
        'series': series,
    }
    
    return render(request, "analyzer/cgpa_level.html", context)

@login_required    
def student_cgpa_analysis(request, student_slug, chartID='container', chart_type = 'area', chart_height=300):
    student = get_object_or_404(Student, slug=student_slug)
    data = cgpaData.get_cgpa('2017', student.id)
    
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'xy'}
    title = {"text": "%s's CGPA Analysis Chart" % (student)}
    xAxis = {"title": {"text": 'Level|(Semester)'}, "categories": data['level']}
    yAxis = {"title": {"text": "Scores Obtained"}, "min": 0, "max": max(cp.get_grades(student.institution)), "tickInterval": 0.5}
    series = [{"name": "Student CGPA", "data": data['cgpa']}]
    
    
    context = {
        'chartID': chartID,
        'chart': chart,
        'title': title,
        'xAxis': xAxis,
        'student': student,
        'yAxis': yAxis,
        'series': series,
    }
    
    return render(request, "analyzer/_analyze_cgpa.html", context)

@login_required
def all_analysis(request, template_name='analyzer/analytics_main.html', chartID='container', chart_type = 'column', chart_height=300):
    #All cgpa analysis
    data_active, data_graduate = cgpaData.get_all_cgpa(institution=request.user.lecturer.institution)
    max_grade = max(cp.get_grades(request.user.lecturer.institution))
    
   #Active Students Charts
    cgpa_chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'xy'}
    cgpa_title = {"text": "Active Students' CGPA"}
    cgpa_xAxis = {"title": {"text": 'Reg Number'}, "categories": data_active['student']}
    cgpa_yAxis = {"title": {"text": "CGPAs"}, "min": 0, "max": max_grade, "tickInterval": 0.5}
    cgpa_series = [{"name": "Student CGPA", "data": data_active['cgpa']}]
    
    #Graduated Students Charts
    g_chart = {"renderTo": "g_charts", "type": "line", "height": chart_height, "zoomType": 'xy'}
    g_title = {"text": "Graduate Students' CGPA"}
    g_xAxis = {"title": {"text": 'Reg Number'}, "categories": data_graduate['student']}
    g_yAxis = {"title": {"text": "CGPAs"}, "min": 0, "max": max_grade, "tickInterval": 0.5}
    g_series = [{"name": "Student CGPA", "data": data_graduate['cgpa']}]
    
    
    students = Student.objects.filter(institution=request.user.lecturer.institution)
    male_students = students.filter(sex='M').count()
    female_students = students.filter(sex='F').count()
    total = students.filter(user_status='A').count()
    suspension = students.filter(user_status='S').count()
    graduated = students.filter(user_status='G').count()
    
    
    #average cgpa analysis by gender
    avg_data = main.average_performance(institution=request.user.lecturer.institution)
    chart = {"renderTo": 'chart_avg', "type": "area", "height": 270, "zoomType": 'xy'}
    title = {"text": "Yearly Average Performance"}
    xAxis = {"title": {"text": 'Year'}, "categories": avg_data['year']}
    yAxis = {"title": {"text": "Average CGPAs"}, "min": 0}
    series = [{"name": "Annual CGPA Average", "data": avg_data['avg_cgpa']}]
    
    #average analysis by courses
    course_data = main.average_course_performance(request.user.lecturer.institution)
    c_chart = {"renderTo": 'c_chart', "type": "column", "height": 270, "zoomType": 'x'}
    c_title = {"text": "Course Overall Performance"}
    c_xAxis = {"title": {"text": 'Courses'}, "categories": course_data['course']}
    c_yAxis = {"title": {"text": "Average"}, "min": 0 }
    c_series = [{"name": "Passes", "data": course_data['passes']}, {"name": "Failures", "data": course_data['failures']}]
    
    
    context = {
        'cgpa_chart': cgpa_chart,
        'cgpa_title': cgpa_title,
        'cgpa_xAxis': cgpa_xAxis,
        'cgpa_yAxis': cgpa_yAxis,
        'cgpa_series': cgpa_series,
        'g_chart': g_chart,
        'g_title': g_title,
        'g_xAxis': g_xAxis,
        'g_yAxis': g_yAxis,
        'g_series': g_series,
        'chart': chart,
        'title': title,
        'xAxis': xAxis,
        'yAxis': yAxis,
        'series': series,
        'c_chart': c_chart,
        'c_title': c_title,
        'c_xAxis': c_xAxis,
        'c_yAxis': c_yAxis,
        'c_series': c_series,
        'males': male_students,
        'females': female_students,
        'total': total,
        'suspension': suspension,
        'graduated': graduated,
    }
    
    return render(request, template_name, context)

@login_required
def student_analysis(request, student_slug, chartID='container', chart_type = 'bar', chart_height=300):
    student = get_object_or_404(Student, slug=student_slug)
    current_level = student.level
    default_level = 100
    max_grade = max(cp.get_grades(student.institution))
    last_passed_level = current_level-default_level
    semester = request.GET.get('semester', 1)
    level = request.GET.get('level', '')
    result = StudentChartData.student_result_data(student.id, current_level) 
    
    #details for previous levels
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'xy'}
    title = {"text": "Student's Curent Level Performance: %s Level" % (current_level)}
    xAxis = {"title": {"text": 'Courses'}, "categories":result['course']}
    yAxis = {"title": {"text": "Scores Obtained"}}
    series = [{'name': 'Scores (%)','data': result['score']}]
    
    #details for current level
    results = Result.objects.filter(student_id=student.id).order_by('level')
    other_result = {'score':[], 'course':[]}
    
    for result in results:
        if result.level != current_level:
            other_result['score'].append(float(result.total_score))
            other_result['course'].append(str(result.course)[:6])
    
    o_chart = {"renderTo": "chart", "type": "column", "height": chart_height, "zoomType": 'x'}
    if last_passed_level == 0:
        o_title = {"text": "No Past Records for %s" % (student)}
    else:  
        if last_passed_level == default_level:
            o_title = {"text": "Student's Previous Level Performance: (%s Level)" % (default_level )}
        else:
            o_title = {"text": "Student's Previous Level Performance: (%s To %s Level)" % (default_level, last_passed_level )}

    o_xAxis = {"title": {"text": 'Courses'}, "categories":other_result['course']}
    o_yAxis = {"title": {"text": "Scores Obtained"}}
    o_series = [{'name': 'Scores (%)','data': other_result['score']}]
    
    #details for the overall grade performance
    grade_result = {'grade':[], 'course':[]}

    for rez in results:
        grade_result['grade'].append(float(rez.course_load/rez.credit_load))
        grade_result['course'].append(str(rez.course)[:6])
    
    v_chart = {"renderTo": "chart", "type": "line", "height": chart_height, "zoomType": 'x'}
    if default_level == current_level:
        v_title = {"text": "%s Overall Course Performance for %s Level" %(student, current_level)}
    else:        
        v_title = {"text": "%s Overall Course Performance From %s To %s Level" % (student, default_level, current_level)}
    v_xAxis = {"title": {"text": 'Courses'}, "categories":grade_result['course'], "lineWidth": 2, "lineColor": "#c14"}
    v_yAxis = {"title": {"text": "Grades Obtained"}, "min": 0, "max": max_grade, "tickInterval": 1, "lineWidth": 2, "lineColor": "#c14"}
    v_series = [{'name': 'Grade Points','data': grade_result['grade']}]  
    
    context = {
        'chartID': chartID, 'chart': chart, 'title': title, 'xAxis': xAxis,
        'student': student, 'yAxis': yAxis, 'series': series, 'chartID': chartID,
        'o_chart': o_chart, 'o_title': o_title, 'o_xAxis': o_xAxis, 'o_yAxis': o_yAxis, 'o_series': o_series,
        'v_chart': v_chart, 'v_title': v_title, 'v_xAxis': v_xAxis, 'v_yAxis': v_yAxis, 'v_series': v_series,
    }
    
    return render(request, "analyzer/_all_results.html", context)
# Create your views here.

def chart_data_json(request):
    data = {}
    params = request.GET

    level = params.get('level', 100)

    data['chart_data'] = ResultData.get_avg_result(level=int(level))

    return HttpResponse(json.dumps(data),"analyzer/_all_results.html", content_type='application/json')


def filter_data(request, chartID='container', chart_type = 'area', chart_height=300):
    
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'xy'}
    title = {"text": "Student Result Analysis Chart"}
    xAxis = {"title": {"text": 'Courses'}, "categories": data['course']}
    yAxis = {"title": {"text": "Scores Obtained"}}
    series = [{"name": "Student Scores", "data": data['score'], "type": "column"}]
    
    context = {
        'chartID': chartID,
        'chart': chart,
        'title': title,
        'xAxis': xAxis,
        'yAxis': yAxis,
        'series': series,
        'new_xAxis': new_xAxis,
        'new_series': new_series
    }
    
    return render(request, "analyzer/_first_main_filter.html", context)


def prediction(request, student_slug, chartID='chart', chart_type='area', chart_height=300):
    student = get_object_or_404(Student, slug=student_slug)
    results = Result.objects.filter(student_id=student.id).order_by('level')
    data = ResultData.get_all_results(student.id)

    chart = {"renderTo": "container", "type": chart_type, "height": chart_height, "zoomType": 'xy'}
    title = {"text": "Current Performance"}
    xAxis = {"title": {"text": 'Courses Offered'}, "categories": data['course']}
    yAxis = {"title": {"text": "Scores"}}
    series = [{"name": "Scores", "data": data['score']}]
    
    context = {
        'chartID': chartID,
        'chart': chart,
        'title': title,
        'xAxis': xAxis,
        'yAxis': yAxis,
        'series': series,
        'student': student,
        'results': results,
    }
    
    return render(request, "analyzer/_predict.html", context)

def make_prediction(request, student_slug):
    student = get_object_or_404(Student, slug=student_slug)
    
    xs = RegressionModel.get_data_X(student.id)
    ys = RegressionModel.get_data_Y(student.id)
    m = "%.4f" % (RegressionModel.best_fit_slope(xs, ys))

    return render(request, 'analyzer/_predict.html', {'mean':ys, 'student': student})


def export_excel(request):
    all_cgpa = main.get_performance_report(request.user.lecturer.institution)
    
    students = Student.objects.filter(institution=request.user.lecturer.institution)
    print(all_cgpa)
    fcgpa = ((student.full_name, student.reg_number, all_cgpa[student.reg_number]) for student in students)
    fields = ["student","reg number","FCGPA"]
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=performance_report.xls"
    report = ExcelReport(fcgpa, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response


# @user_passes_test(user_is_staff, login_url='/login/')
@login_required
def get_json_data(request):
    data = None
    params = request.GET
    data_active, data_graduate = cgpaData.get_all_cgpa(institution=request.user.lecturer.institution)

    level = params.get('level', '')
    course_id = params.get('course', '')
    semester = params.get('semester', '')
    dept_id = params.get('dept', 'all')
    name = params.get('name', '')
    year = params.get('year', '')

    if name == 'cgpa_data':
        dept=None
        results = None
        if dept_id != 'all':
            dept = Department.objects.get(pk=dept_id)
            results = Result.objects.filter(course=course, department=dept, 
                                            date_created__year=year)
            data = ResultData.get_result_by_lecturer(results)
        else:
            results = Result.objects.filter(course__lecturers=request.user.lecturer, 
                                            course=course,
                                            date_created__year=year)
            data = ResultData.get_result_by_lecturer(results)
    elif name == 'course_average_by_dept':
        data = ResultData.dept_avg_score(course)
        data = main.average_performance(institution=request.user.lecturer.institution)
    elif name == 'active_student':
        dept=None
        results=ResultData.get_all(request.user.lecturer.institution)
        if dept_id != 'all':
            dept = Department.objects.get(pk=dept_id)
            results = results.filter(department=dept)
            data = ResultData.get_result_by_lecturer(results)
        if level !='' or level is not None:
            results = results.filter(level=level)
            data = ResultData.get_result_by_lecturer(results)
        if year !='all':
            results = results.filter(date_created__year=year)
    elif name == 'graduate_student':
        dept=None
        results=ResultData.get_all(request.user.lecturer.institution)
        if dept_id != 'all':
            dept = Department.objects.get(pk=dept_id)
            results = results.filter(department=dept)
            data = ResultData.get_result_by_lecturer(results)
        if level !='' or level is not None:
            results = results.filter(level=level)
            data = ResultData.get_result_by_lecturer(results)
    return HttpResponse(json.dumps(data), content_type='application/json')

