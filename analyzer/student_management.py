from django.contrib.auth.decorators import login_required
from .utils import ChartData, cgpaData
from students.models import Student


@login_required
def all_analysis(template_name, chartID='container', chart_type = 'column', chart_height=300):
    #All cgpa analysis
    data = cgpaData.get_all_cgpa()
   
    cgpa_chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'xy'}
    cgpa_title = {"text": "My CGPA Breakdown"}
    cgpa_xAxis = {"title": {"text": 'Reg Number'}, "categories": data['student']}
    cgpa_yAxis = {"title": {"text": "CGPAs"}, "min": 0, "max": 5, "tickInterval": 0.5}
    cgpa_series = [{"name": "Student CGPA", "data": data['cgpa']}]
    
    male_students = Student.objects.filter(sex='M').count()
    female_students = Student.objects.filter(sex='F').count()
    total = Student.objects.filter(user_status='A').count()
    suspension = Student.objects.filter(user_status='S').count()
    graduated = Student.objects.filter(user_status='G').count()
    
    
    #average cgpa analysis by gender
    avg_data = main.average_performance()
    chart = {"renderTo": 'chart_avg', "type": "column", "height": 270, "zoomType": 'xy'}
    title = {"text": "My Yearly Average Performance"}
    xAxis = {"title": {"text": 'Year'}, "categories": avg_data['year']}
    yAxis = {"title": {"text": "Average CGPAs"}, "min": 0}
    series = [{"name": "Males", "data": avg_data['male']},
        {"name": "Female", "data": avg_data['female']}]
    
    #average analysis by courses
    course_data = main.average_course_performance()
    c_chart = {"renderTo": 'c_chart', "type": "column", "height": 270, "zoomType": 'x'}
    c_title = {"text": "My Overall Course Performance"}
    c_xAxis = {"title": {"text": 'Courses'}, "categories": course_data['course']}
    c_yAxis = {"title": {"text": "Average"}, "min": 0 }
    c_series = [{"name": "Passes", "data": course_data['passes']}, {"name": "Failures", "data": course_data['failures']}]
    
    
    context = {
        'cgpa_chart': cgpa_chart,
        'cgpa_title': cgpa_title,
        'cgpa_xAxis': cgpa_xAxis,
        'cgpa_yAxis': cgpa_yAxis,
        'cgpa_series': cgpa_series,
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
    
    return context