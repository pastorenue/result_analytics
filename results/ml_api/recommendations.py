from math import *
from students.models import Student
from results.models import Result
from results.utils import Computation as cp
from analyzer.utils import cgpaData
import operator

#The data in each of these functions will be in the range of 0-10
#so that the calculations will not take too much memory space
def euclidean_distance_score(data, student1, student2):
	#get the similaritities in the grades
	similarity = []
	for course in data[student1]:
		if course in data[student2]:
			similarity.append(1)
	#if not related grade range, return 0
	if len(similarity) == 0:
		return 0

	sum_of_squares =  sum([pow(data[student1][course]-data[student2][course], 2) 
							for course in data[student1] if course in data[student2]])
	return 1/(1 + sum_of_squares)


def cosine_similarity(data, student1, student2):
	def square_rooted(student):
		return round((sqrt(sum([pow(data[student][a], 2) for a in data[student]]))), 3)

	numerator = sum(data[student1][course] * data[student2][course] for course in data[student1] if course in data[student2])
	denominator = square_rooted(student1) * square_rooted(student2)
	if denominator == 0:
		return 0
	return numerator/denominator


def sim_pearson(data, student1, student2):	
	similarity = {}
	for course in data[student1]:
		if course in data[student2]:
			similarity[course] = 1
	if len(similarity) < 1: 
		return	0

	#Add up all courses
	sum_student1 = sum([data[student1][course] for course in similarity])
	sum_student2 = sum([data[student2][course] for course in similarity])

	#Sum up the squares
	sq_sum_student1 = sum([pow(data[student1][course], 2) for course in similarity])
	sq_sum_student2 = sum([pow(data[student2][course], 2) for course in similarity])

	#Sum up the product
	all_product_sum = sum([data[student1][course] * data[student2][course] for course in similarity])

	#Calculating the Pearson euclidean_distance_score
	N = len(similarity)
	numerator = N*all_product_sum-(sum_student1*sum_student2)
	denominator = sqrt((N*sq_sum_student1-pow(sum_student1, 2))*(N*sq_sum_student2-pow(sum_student2, 2)))

	if denominator == 0:
		return 0
	return numerator/denominator


def top_matches(data, student, length=4, algorithm=None, reverse=False):
	"""This returns the closest match to the student specified"""
	ranks = [[other, algorithm(data, student, other)] for other in data if other != student]
	ranks.sort(key=operator.itemgetter(1))
	if reverse:
		ranks.reverse()
	return ranks[:length]


def get_recommendations(data, student, algorithm=euclidean_distance_score, reverse=True):
	totals = {}
	sim_sum = {}
	for other in data:
		courses = []
		sims = []
		if other == student:
			continue
		sim = algorithm(data, student, other)
		if sim <= 0:
			continue
		for course in data[other]:
			if course in data[student]:
				courses.append(data[other][course] * sim)
				sims.append(sim)
		totals[other] = sum(courses)
		sim_sum[other] = sum(sims)
	ranking = [[total/sim_sum[other], other] for other,total in totals.items()]
	ranking.sort(key=operator.itemgetter(1))
	if reverse:
		ranking.reverse()
	return ranking 


def transform_data(data):
	new_data = {}
	for student in data:
		for course in data[student]:
			new_data.setdefault(course, {})

			new_data[course][student] = data[student][course]
	return new_data


def get_result_queryset(student):
	return Result.objects.filter(student=student)

def get_dataset(request, course=None, use_cgpa=True):
	data = {}
	students = None
	active_students = [student for student in Student.objects.all() if student.user.studentsetup.allow_my_result_for_analysis]
	preferred_students =[student for student in Student.objects.all() if cgpaData.get_fcgpa(student.id) >= float(0.75*max(cp.get_grades(student.institution))) and 
							student.user.studentsetup.allow_my_result_for_analysis]
	if use_cgpa:
		students = preferred_students
		if request.user.student not in students:
			students.append(request.user.student)
	else:
		students = active_students	
	for student in students:
		tmp_data = {}
		results = None
		if course:
			results = get_result_queryset(student).filter(course=course)
		else:
			results = get_result_queryset(student)
		for result in results:
			tmp_data[result.course] = float(result.total_score)/10
		data[student] = tmp_data

	return data