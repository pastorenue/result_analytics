from results.models import CGPA, Result
from students.models import Student
from django.db.models import Sum, Aggregate, FloatField
from statistics import mean
from courses.models import Course
from decimal import Decimal
from results.utils import Computation as cp

class MainData(object):
    
    @classmethod
    def get_performance_report(cls, institution):
        students = Student.objects.filter(institution=institution)
        data = {}
        
        for student in students:
            gpa = cgpaData.get_fcgpa(student.id)
            st = student.reg_number
            data[st]= float(gpa)
        return data
    
    @classmethod
    def yearly_data(cls):
        #data = {'year':[], 'male':[], 'female':[], 'passes':[], 'failures', 'performance':[]}
        pass
    
    @classmethod
    def average_performance(cls, institution, **kwargs):
        data = {'year':[], 'avg_cgpa':[]}
        res = Result.objects.filter(institution=institution)
        years = []
        students = Student.objects.filter(institution=institution)
        for student in students:
            if student.year_of_admission.year in years:
                pass
            else:
                years.append(student.year_of_admission.year)
        years.sort()
        for year in years:
            avg_cgpa = []
            for student in students:
                avg_cgpa.append(cgpaData.get_cgpa(year, student.id))
            data['year'].append(year)
            data['avg_cgpa'].append("%.2f" % float(sum(avg_cgpa)/len(avg_cgpa)))       
        return data
    
    @classmethod
    def average_course_performance(cls, institution, **kwargs):
        data = {'course':[], 'passes':[], 'failures':[]}
        
        student = Student.objects.filter(institution=institution)
        courses = Course.objects.all().order_by('course_code')
        for course in courses:
            passes = 0
            failures = 0
            res = Result.objects.filter(course=course)
            for r in res:
                if r.total_score>=55:
                    passes+=1
                else:
                    failures+=1
            data['course'].append(course.course_code)
            data['passes'].append(passes)
            data['failures'].append(failures)
        
        return data
        
        
class StudentChartData(object):
    def all_result_data(**kwargs):
        data = {'level':[], 'grade':[]}
        
        values = Result.objects.all()
        
        for value in values:
            data['level'].append(value.level)
            data['grade'].append(value.cgpa)
        
        return data
    
    @classmethod
    def student_result_data(cls, id, level):
        data = {'course':[], 'score':[]}
        records = Result.objects.filter(student_id=id, level=level).order_by('-course')
        
        for value in records:
            data['course'].append(str(value.course)[:6])
            data['score'].append(float(value.total_score))
        
        return data
        
class ResultData(object):

    @classmethod
    def get_all(cls, institution):
        return Result.objects.filter(institution=institution)
    
    @classmethod
    def get_result_by_level(cls, student_id, **kwargs):
        data = {'level':{'course': [], 'score': []}}
        for i in range(100,600,100):
            results = Result.objects.filter(student_id=student_id, level=i).order_by('level')
            data['level'].append(i)
            for avg in results:
                data['level'][i]['score'].append(avg.total_score)
                data['level'][i]['course'].append(avg.course)
        return data
    
    @classmethod
    def get_result_by_semester(cls, student_id, semester, level, **kwargs):
        results = Result.objects.filter(semester=semester, level=level, student_id=student_id).values('score').distinct()
        
        data = {'score':[], 'course':[]}
        for result in results:
            data['score'].append(result.total_score)
            data['course'].append(result.course)
        return data
    
    @classmethod
    def get_result_by_student(cls, student_id):
        results = Result.objects.filter(student_id=student_id).order_by('level')
        data = {'score': [], 'course': []}
        
        for value in results:
            data['score'].append(value.total_score)
            data['course'].append(value.course)
        return data
    
    @classmethod
    def grader(cls, course_load, credit_load):
        grade = {}
        from results.models import Grading
        
        all_grades = Grading.objects.all()
        for grad in all_grades:
            grade[grad.grade_points] = grad.caption
        
        record_grade = course_load/credit_load
        return grade[record_grade]

    @classmethod
    def get_all_results(cls, student_id):
        results = Result.objects.filter(student_id=student_id).order_by('level')
        data = {'course':[], 'score':[]}
        
        for value in results:
            data['course'].append(str(value.course)[:6])
            data['score'].append(float(value.total_score))
        return data

    @classmethod
    def get_result_by_lecturer(cls,results):
        data = {'reg_number':[], 'exam_score':[], 'assignment_score':[], 'quiz_score':[]}

        for result in results:
            temp_data = {}
            data['exam_score'].append(float(result.exam_score))
            data['assignment_score'].append(float(result.assignment_score))
            data['quiz_score'].append(float(result.quiz_score))
            data['reg_number'].append((result.student.reg_number))
        return data

    @classmethod
    def dept_avg_score(cls, lecturer, course):
        results = Result.objects.filter(course__lecturers=lecturer, course=course)
        dept_list = []
        for result in results:
            if result.student.department not in dept_list:
                dept_list.append(result.student.department)
        data = {'department':[], 'average': []}
        for dept in dept_list:
            scores = []
            for res in results:
                if res.student.department == dept:
                    scores.append(res.total_score)
            data['department'].append(dept.code)
            data['average'].append(float(sum(scores)/len(scores)))
        return data 

    @classmethod
    def dept_avg_performance(cls, lecturer, course, dept):
        results = Result.objects.filter(course__lecturer=lecturer, course=course)
        dept_list = []
        for result in results:
            if result.student.department not in dept_list:
                dept_list.append(result.student.department)
        data = {'department':[], 'passes': [], 'fails':[]}

        for dept in dept_list:
            passes = 0
            fails = 0
            for res in results:
                if res.student.department == dept:
                    if res.total_score > 50: # I need th make the value dynamic
                        passes+=1
                    else:
                        fails+=1
            data['department'].append(dept)
            data['passes'].append(passes)
            data['fails'].append(fails)
        return data


class cgpaData(object):
    
    @classmethod
    def get_cgpa(cls,year,student_id):
        result = Result.objects.filter(date_created__year = year, student_id=student_id)
        course_load = result.aggregate(course = Sum('course_load', output_field=FloatField()))['course'] or 0
        credit_load = result.aggregate(credit = Sum('credit_load', output_field=FloatField()))['credit'] or 0
        grade = 0.0
        if course_load!= 0 or None:
            grade = '%.2f' % (course_load/credit_load)
        
        return float(grade)
   
    @classmethod
    def get_all_cgpa(cls, institution):
        students = Student.objects.filter(institution=institution)
        active_students = students.filter(user_status='A').order_by('department')
        graduate_students = students.filter(user_status='G').order_by('department')
        data_active = {'student': [], 'cgpa': []}
        data_graduate ={'student': [], 'cgpa': []}
        
        for student in active_students:
            data_active['student'].append('%s' % (str(student.reg_number)))
            data_active['cgpa'].append(float(cgpaData.get_fcgpa(student.id)))
            
        for student in graduate_students:
            data_graduate['student'].append('%s' % (str(student.reg_number)))
            data_graduate['cgpa'].append(float(cgpaData.get_fcgpa(student.id)))
        return data_active, data_graduate
    
    @classmethod
    def get_level_cgpa(cls, level, student_id):
        result = Result.objects.filter(level=level, student_id=student_id)
        course_load = result.aggregate(course = Sum('course_load', output_field=FloatField()))['course']
        credit_load = result.aggregate(credit = Sum('credit_load', output_field=FloatField()))['credit']
        
        grade = '%.2f' % (course_load/credit_load)
        return float(grade)
    
    @classmethod
    def get_fcgpa(cls, student_id):
        result = Result.objects.filter(student_id=student_id)
        course_load = result.aggregate(course = Sum('course_load', output_field=FloatField()))['course'] or 0
        credit_load = result.aggregate(credit = Sum('credit_load', output_field=FloatField()))['credit'] or 0
        student = Student.objects.get(id=student_id)
        grade = 0
        if result.exists():
            if course_load==0:
                grade = 0
            else:
                grade = '%.2f' % (course_load/credit_load)
        else:
            grade = float(max(cp.get_grades(student.institution)))
        return float(grade)
            
    
    #@classmethod
    # def get_cgpa_by_semester(cls, semester, student_id, level):
    #     result = Result.objects.filter(semester=semester, level=level, student_id=student_id)
    #     course_load = result.aggregate(course = Sum('course_load', output_field=FloatField()))['course']
    #     credit_load = result.aggregate(credit = Sum('credit_load', output_field=FloatField()))['credit']
        
    #     grade = '%.2f' % (course_load/credit_load)
    #     return float(grade)


    def grader():
        pass
    
class RegressionModel(object):
    
    @classmethod
    def get_data_Y(cls, student_id):
        level = []
        data = []
        res = Result.objects.filter(student_id=student_id)
        for r in res:
            level.append(r.level) 
        sorted(level)
        
        for i in [100, 200, 300, 400]:
            for x in [1,2]:
                data.append(cgpaData.get_cgpa_by_semester(x, student_id, i))
        return data
    
    @classmethod   
    def get_data_X(cls):
        level = []
        data = []
  
        for x in [100, 200, 300, 400]:
            for i in [1, 2]:
                data.append(cgpaData.get_units_by_semester(i, x))
        return data
    
    @classmethod   
    def best_fit_slope_and_intercept(cls, X, Y):
        xy = [x*y for x,y in zip(X,Y)]
        xx = [x**x for x in X]
        m = ((mean(X)* mean(Y))-(mean(xy))/((mean(X))**2)-mean(xx))
        b = mean(Y) - m*mean(X)
        return m, b



def pin_generator(length=8):
    
    '''
    This is to generate alphanumeric ids for the transaction. the addition of non-alphameric chars increases the uniqueness of the transaction id e.g Qw21#d seem more unique than 1242
    
    It can also serve as a secrete key generator of any length.
    '''
    
    import random
    
    num = '0123456789'
    chars = '@#$&'
    upper_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_alpha = upper_alpha.lower()
    gen_base = [num,chars,upper_alpha,lower_alpha]
    alphanum = ''.join(gen_base)
    
    transaction_id = ''
    
    for x in range(length):
        transaction_id += alphanum[random.randint(1,len(alphanum)-1)]
    
    return transaction_id 
 

def decimal_add(x, y):
    '''
    This is an operator for a decimal addition. 
    '''
    return Decimal(x) + Decimal(y)