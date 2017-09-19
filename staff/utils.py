from results.models import Result
from students.models import Student
from .models import Lecturer
from django.db import transaction
from courses.models import Course
def user_is_staff(user):
	return user.is_staff


def staff_analytics_metrics(user):
	lecturer = Lecturer.objects.get(user=user)
	results = Result.objects.filter(course__lecturer=lecturer)
	student_list = []

	for student in Student.objects.filter(institution=user.lecturer.institution):
		for result in results:
			if student in student_list:
				continue
			else:
				student_list.append(student)

	context = {
		'total_results': results.count(),
		'students_attending_to': len(student_list)
	}

	return context

@transaction.atomic
def import_quiz_from_csv(csv_file, lecturer):
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
    header_check = ['student', 'course', 'score', 'level', 'semester', 'session']
    first_row = [i.lower().strip() for i in csv_data[0]]
    if all(i in first_row for i in header_check):
        csv_data = csv_data[1:]
    
    new_value = 0 # To get the number of records entered
    update_value = 0

    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        if row:
            student = Student.objects.get(reg_number=row[0])
            course = Course.objects.get(course_code = str(row[1]).upper(), lecturer=lecturer)
            exiting = Quiz.objects.filter(student=student, course=course,level=row[3],semester=row[4])
            if exiting.count() > 0:
                if existing[0].score == 0.0:
                	exiting[0].score = row[2]
	                existing[0].save()
	                update_value+=1
            else:
                Quiz.objects.create(
                    student=student,
                    course=course,
                    score=row[2],
                    level=row[3],
                    semester=row[4],
                    session=row[5],
                )
                new_value+=1			
    return new_value



@transaction.atomic
def import_all_from_csv(csv_file, lecturer):
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
    header_check = ['student', 'course', 'assignment_score', 'quiz_score', 'exam_score', 'level', 'semester', 'session']
    first_row = [i.lower().strip() for i in csv_data[0]]
    if all(i in first_row for i in header_check):
        csv_data = csv_data[1:]
    
    new_value = 0 # To get the number of records entered
    update_value = 0

    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        if row:
            student = Student.objects.get(reg_number=row[0])
            course = Course.objects.get(course_code = str(row[1]).upper(), lecturer=lecturer)
            exiting = Result.objects.filter(student=student, course=course,level=row[5],semester=row[6])
            if exiting.count() > 0:
                if existing[0].quiz_score == 0.0:
                	exiting[0].quiz_score = row[3]
                if existing[0].exam_score == 0.0:
                	existing[0].exam_score = row[4]
                if existing[0].assignment_score == 0.0:
                	existing[0].assignment_score = row[2]
                existing[0].save()
                update_value+=1
            else:
                Result.objects.create(
                    student=student,
                    course=course,
                    assignment_score=row[2],
                    quiz_score=row[3],
                    exam_score=row[4],
                    level=row[5],
                    semester=row[6],
                    session=row[7],
                )
                new_value+=1			
    return new_value


@transaction.atomic
def import_assignment_from_csv(csv_file, lecturer):
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
    header_check = ['student', 'course', 'score', 'level', 'semester', 'session']
    first_row = [i.lower().strip() for i in csv_data[0]]
    if all(i in first_row for i in header_check):
        csv_data = csv_data[1:]
    
    count_value = 0 # To get the number of records entered

    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        if row:
            student = Student.objects.get(reg_number=row[0])
            course = Course.objects.get(course_code = str(row[1]).upper(), lecturer=lecturer)
            assignment = AssignmentScore.objects.get(student=student)
            if assignment:
                if assignment.status == 'M':
                	pass
                elif assignment.status == 'S':
                	assignment.score = row[2]
                	assignment.status = 'M'
                	assignment.save()
	                count_value+=1		
    return count_value

def generate_mapper():
    pass