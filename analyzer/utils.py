from results.models import CGPA, Result
from students.models import Student
from django.db.models import Sum, Aggregate, FloatField
from statistics import mean
from courses.models import Course

class MainData(object):
    
    @classmethod
    def get_performance_report(cls):
        students = Student.objects.all()
        data = {}
        
        for student in students:
            gpa = cgpaData.get_fcgpa(student.id)
            st = student.reg_number
            data[st]= gpa
        return data
    
    @classmethod
    def yearly_data(cls):
        #data = {'year':[], 'male':[], 'female':[], 'passes':[], 'failures', 'performance':[]}
        pass
    
    @classmethod
    def average_performance(cls):
        data = {'year':[], 'male':[], 'female':[]}
        male = []
        female = []
        res = Result.objects.all()
        students = Student.objects.all()
        for student in students:
            if student.sex == 'F':
                female.append(cgpaData.get_cgpa(2016, student.id))
            else:
                male.append(cgpaData.get_cgpa(2016, student.id))
                
        data['male'].append(sum(male)/len(male))
        data['female'].append(sum(female)/len(female))
        data['male'].append(4.6)
        data['female'].append(4.7)
        data['year'].append(2015)
        data['year'].append(2016)
        
        return data
    
    @classmethod
    def average_course_performance(cls):
        data = {'course':[], 'passes':[], 'failures':[]}
        
        student = Student.objects.all()
        courses = Course.objects.all().order_by('course_code')
        for course in courses:
            passes = 0
            failures = 0
            res = Result.objects.filter(course=course)
            for r in res:
                if r.score>=55:
                    passes+=1
                else:
                    failures+=1
            data['course'].append(course.course_code)
            data['passes'].append(passes)
            data['failures'].append(failures)
        
        return data
        
        
class ChartData(object):
    def all_result_data():
        data = {'level':[], 'grade':[]}
        
        values = Result.objects.all()
        
        for value in values:
            data['level'].append(value.level)
            data['grade'].append(value.cgpa)
        
        return data
    
    def student_result_data(id, level):
        data = {'course':[], 'score':[]}
        records = Result.objects.filter(student_id=id, level=level).order_by('-course')
        
        for value in records:
            data['course'].append(str(value.course)[:6])
            data['score'].append(float(value.score))
        
        return data
        
class ResultData(object):
    
    @classmethod
    def get_result_by_level(cls, student_id):
        data = {'level':{'course': [], 'score': []}}
        for i in range(100,600,100):
            results = Result.objects.filter(student_id=student_id, level=i).order_by('level')
            data['level'].append(i)
            for avg in results:
                data['level'][i]['score'].append(avg.score)
                data['level'][i]['course'].append(avg.course)
        return data
    
    @classmethod
    def get_result_by_semester(cls, student_id, semester, level):
        results = Result.objects.filter(semester=semester, level=level, student_id=student_id).values('score').distinct()
        
        data = {'score':[], 'course':[]}
        for result in results:
            data['score'].append(result.score)
            data['course'].append(result.course)
        return data
    
    @classmethod
    def get_result_by_student(cls, student_id):
        results = Result.objects.filter(student_id=student_id).order_by('level')
        data = {'score': [], 'course': []}
        
        for value in results:
            data['score'].append(value.score)
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
            data['score'].append(float(value.score))
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
    def get_all_cgpa(cls):
        active_students = Student.objects.filter(user_status='A').order_by('department')
        graduate_students = Student.objects.filter(user_status='G').order_by('department')
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
        
        grade = 0
        if course_load==0:
            grade = 0
        else:
            grade = '%.2f' % (course_load/credit_load)
        return float(grade)
            
    
    @classmethod
    def get_cgpa_by_semester(cls, semester, student_id, level):
        result = Result.objects.filter(semester=semester, level=level, student_id=student_id)
        course_load = result.aggregate(course = Sum('course_load', output_field=FloatField()))['course']
        credit_load = result.aggregate(credit = Sum('credit_load', output_field=FloatField()))['credit']
        
        grade = '%.2f' % (course_load/credit_load)
        return float(grade)
    
    @classmethod
    def get_result_by_lecturer(cls,lecturer):
        results = Result.objects.filter(course__lecturer=lecturer)
        data = {'score': [], 'student':[]}

        return data
    
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

    
    #code

    