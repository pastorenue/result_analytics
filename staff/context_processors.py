from results.models import Result
from institutions.models import Department, Lecturer
from students.models import Student
from django.db.models import *

def home_context(request):
    
    all_students = Student.objects.all()
    departments = Department.objects.all()
    lecturers = Lecturer.objects.all ()
    all_results = Result.objects.all()
    
    avg_performance = Result.objects.aggregate(avg = Avg('score'))['avg'] or 0
    count = Result.objects.all().order_by('score')[:10]
    
    ranking = int(avg_performance*0.1) or 0
    
    
    return {
        'deparmments': departments,
        'lecturers': lecturers,
        'avg_performance': avg_performance,
        'ranking': ranking,
        'all_students': all_students,
        'all_results': all_results,
        'count': count,
    }
