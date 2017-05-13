from django.db.models import Sum, Value
from .models import Result, Grading
import csv
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

def import_result_from_csv(csv_file):
    """
    Import result CSV data.

    We'll process all rows first and create Result model objects from them
    and perform a bulk create. This way, no records will be inserted unless
    all records are good.
    
    """
    csv_data = []
    
    rows = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in rows:
        csv_data.append([item.strip() for item in row])
    
    result_objects = []

    # Check if headers exists. Skip the first entry if true.
    header_check = ['reg_number', 'course', 'score', 'level', 'semester', 'session']
    first_row = [i.lower().strip() for i in csv_data[0]]
    if all(i in first_row for i in header_check):
        csv_data = csv_data[1:]

    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        if row:
            student = Student.objects.get(reg_number=row[0])
            course = Course.objects.get(course_code = row[1])
            credit_load = course.unit
            end = min([grade.end for grade in Grading.objects.all() if grade.end >= int(row[2])])
            gd = Grading.objects.filter(end=end)
            grading = Grading.objects.get(caption=gd[0])
            pts = grading.grade_points
            course_load = credit_load*pts
            tmp_result = Result(
                student=student,
                course=course,
                score=row[2],
                credit_load=credit_load,
                course_load = course_load,
                level=row[3],
                semester=row[4],
                session=row[5],
            )
            result_objects.append(tmp_result)


    Result.objects.bulk_create(result_objects)