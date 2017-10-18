from django.db.models import Sum, Value
from django.db import transaction
from .models import Result, Grading
import csv
import codecs
from students.models import Student
from courses.models import Course


class Computation(object):

    @classmethod
    def get_grades(cls, institution):
        grades = Grading.objects.filter(institution=institution)
        data = [float(grade.grade_points) for grade in grades]
        data.append(0.0)
        sorted(data)
        return data


    @classmethod
    def get_cgpa_comment(cls, institution, fcgpa, computation_type=None):
        FIVE_POINT, FOUR_POINT, THREE_POINT = range(5, 2, -1)
        TEST_POINT = 0.0
        scale = {5.0:FIVE_POINT, 4.0:FOUR_POINT, 3.0:THREE_POINT, 0.0:TEST_POINT}

        max_grade_point = max(cls.get_grades(institution))
        degree = ""
        if scale[max_grade_point] == FIVE_POINT:
            if fcgpa >=4.5:
                degree = "currently on FIRST CLASS"
            elif fcgpa>=3.5:
                    degree = "currently on SECOND CLASS-UPPER DIVISION"
            elif fcgpa>=2.5:
                degree = "currently on SECOND CLASS-LOWER DIVISION"
            elif fcgpa>=1.5:
                degree = "currently on THIRD CLASS"
            else:
                degree = "might be graduating with a PASS"
        if scale[max_grade_point] == FOUR_POINT:
            if fcgpa >= 3.5:
                degree = "currently on FIRST CLASS"
            elif fcgpa >= 3.0 and fcgpa <= 3.49:
                degree = "currently on SECOND CLASS-UPPER DIVISION"
            elif fcgpa >= 2.0 and fcgpa <= 2.99:
                degree = "currently on SECOND CLASS-LOWER DIVISION"
            else:
                degree = "on a PASS"
        if scale[max_grade_point] == TEST_POINT:
            degree = "Your school has not set a grading scheme yet. Just be patient"
        return degree

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
                    institution=lecturer.institution,
                    exam_score=row[2],
                    level=row[3],
                    semester=row[4],
                    session=row[5],
                )
                new_value+=1
    return new_value, update_value

def update_results(institution):
    for result in Result.objects.filter(institution=institution):
        result.save()