from django.db.models import Sum, Value
from django.db import transaction
from .models import Result, Grading
import csv
import codecs
from students.models import Student
from courses.models import Course
class Computation(object):
    
    @classmethod
    def get_cgpa(cls, student_id):
        data = Result.objects.filter(student_id=student_id)
        
        units = 1
        grade = 1
        for value in data:
            grade = grade + float(value.get_course_load)
            units = units + float(value.get_credit_load)
        
        cgpa = grade/units
        
        if units!=0 or grade!=0:
            return cgpa

@transaction.atomic
def import_result_from_csv(csv_file, lecturer):
    """
    Import result CSV data.

    We'll process all rows first and create Result model objects from them
    and perform a bulk create. This way, no records will be inserted unless
    all records are good.
    
    """
    csv_data = []
    ifile = csv_file.read().decode("utf-8")
    for row in ifile.split('\n'):
        csv_data.append(row.split(','))
    
    result_objects = []
    print(csv_data)
    # Check if headers exists. Skip the first entry if true.
    header_check = ['student', 'course', 'exam_score', 'level', 'semester', 'session']
    first_row = [i.lower().strip() for i in csv_data[0]]
    if all(i in first_row for i in header_check):
        csv_data = csv_data[1:]
    
    new_value = 0
    update_value = 0 # To get the number of records entered
    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        if row:
            student = Student.objects.get(reg_number=row[0])
            course = Course.objects.get(course_code = str(row[1]).upper(), lecturer=lecturer)
            exiting = Result.objects.filter(student=student, course=course, exam_score=row[2],level=row[3],semester=row[4])
            if exiting.count() > 0:
                if existing[0].exam_score == 0.0:
                    existing[0].exam_score = row[2]
                    existing[0].save()
                    update_value+=1
            else:
                Result.objects.create(
                    student=student,
                    course=course,
                    exam_score=row[2],
                    level=row[3],
                    semester=row[4],
                    session=row[5],
                )
                new_value+=1
    return new_value, update_value