from results.models import Result
from institutions.models import Department, Faculty, Institution
from students.models import Student
from .models import Lecturer
from django.db.models import *
from forum.models import Category
from analyzer.utils import cgpaData
from results.ml_api.recommendations import *
from django.contrib.auth.decorators import login_required
from staff.models import Lecturer
from courses.models import Course
from friendship.models import Friend
from results.utils import Computation as cp
import random
from django.contrib import auth

def home_context(request): 
    all_greetings = [
                    'Hi', 'Ekabo', 'Sannu', 
                    'Bonjour', 'Mavo', 'Ado', 'Ibaate', 
                    'Koyo', 'Bawo ni',
                    'Abole', 'Kedu', 'Ola']
    greeting = all_greetings[random.randint(0, len(all_greetings)-1)]  
    all_students = []
    lecturers = []
    all_results = []
    if request.user.is_authenticated():
        if hasattr(request.user, 'lecturer'):
            all_students = Student.objects.filter(institution=request.user.lecturer.institution)
            lecturers = Lecturer.objects.filter(institution=request.user.lecturer.institution)
            all_results = Result.objects.filter(institution=request.user.lecturer.institution)
    topics = Category.objects.all()[:10]
    departments = Department.objects.all()
    courses = []
    if request.user.is_authenticated():
        courses = Course.objects.filter(added_by=auth.get_user(request))
    avg_performance = Result.objects.aggregate(avg = Avg('exam_score'))['avg'] or 0

    ranking = int(avg_performance*0.1) or 0
    
    
    return {
        'departments': departments,
        'faculties': Faculty.objects.all(),
        'avg_performance': avg_performance,
        'ranking': ranking,
        'all_students': all_students,
        'all_courses': courses,
        'institutions': Institution.objects.all(),
        'all_results': all_results,
        'topics': topics,
        'lecturers': lecturers,
        'greet': greeting

    }

def performances(request):
    performance_list = {}
    for student in Student.objects.all():
        tmp_dict = {}
        tmp_dict['name']=student
        tmp_dict['department']=student.department
        tmp_dict['reg_number']=student.reg_number
        tmp_dict['user']=student.user
        try:
            tmp_dict['are_friends'] = Friend.objects.are_friends(request.user, student.user)
        except:
            pass
        if student.photo:
            tmp_dict['img']=student.photo
        else:
             tmp_dict['img']='None'
        tmp_dict['institution'] = student.institution
        if student.result_set.count() > 0:
            tmp_dict['cgpa'] = cgpaData.get_fcgpa(student.id)
        else:
            tmp_dict['cgpa'] = float(max(cp.get_grades(student.institution)))
        performance_list[student] = tmp_dict
    
    key_list = sorted(performance_list.keys(), key=lambda x: performance_list[x]['cgpa'], reverse=True)
    trending_performances = []
    current_student_rank = None
    count = 0
    for key in key_list:
        count+=1
        if not request.user.is_anonymous() and hasattr(request.user, 'student'):
            if key == request.user.student:
                current_student_rank = count
        trending_performances.append(performance_list[key])
    return {
        'trending_performances': trending_performances[:5],
        'student_rank': current_student_rank,
    }

  
def course_recommendation(request):
    try:
        own_student = request.user.student
    except:
        pass
    courses = {}
    data = {}
    is_new = True
    if request.user.is_authenticated() and  hasattr(request.user, 'student'):
        for result in Result.objects.filter(student=request.user.student):
            if result.total_score < 62.5 and cgpaData.get_fcgpa(own_student.id) < float(max(cp.get_grades(own_student.institution)) * 0.8):
                courses[result.course] = result.total_score
        #get the recommendation for each poorly performed course
        for course in courses:
            dataset = get_dataset(request, course=course)
            matches = top_matches(dataset, request.user.student, length=5, algorithm=euclidean_distance_score)
            data['match'] = matches
    if hasattr(request.user, 'student'):
        is_new = not Result.objects.filter(student=request.user.student).exists()
    return {'recommendations': data, 'student_is_new': is_new }


def performance_recommendation(request):
    if request.user.is_authenticated() and hasattr(request.user, 'student'):
        dataset = get_dataset(request)
        matches = top_matches(dataset, request.user.student, length=5, algorithm=euclidean_distance_score)
        return dict(matches)
    else: 
        return {}

    