from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import ChartData, cgpaData
from students.models import Student
from assignments.models import Assignment
from students.utils import user_is_student

def get_assignment_metrics(lecturer, **kwargs):
	data = {'courses':[], 'passes':0, 'failures':0, 'unsubmitted':[]}
	assignments = Assignment.objects.filter(lecturer=lecturer)
	courses = []

	for course in Course.objects.filter(lecturer=lecturer):
		if course in courses:
			pass
		else:
			courses.append(course)
	for course in courses:
		for assignment in assignments.filter(course=course):
			data['courses'].append(course)
			if assignment.score > assignment.standard:
				data['passes'] += 1
			else:
				data['failures'] += 1
	return data


class BaseChartAPI(object):
	"""Chart API for plotting HighChartjs charts using django"""

	def __init__(self, chart_type, chart_height):
		"""
		The intance of the class will take two arguments
		chart_type: The type of chart to plot
					should be a string
		chart_height: A integer of the height of the chart to be plotted
		"""
		self._chart_type = chart_type
		self._chart_height = chart_height
		self._title = ''
		self._zoom_types = [None, 'x', 'xy', 'y']
		self._zoom = None
		self._queryset = None


	def get_chart_type(self):
		return self._chart_type

	def set_zoom(self, zoom):
		if zoom in self._zoom_types and type(zoom) == 'str':
			self._zoom = zoom

	def get_zoom(self):
		if self._zoom is not None:
			return self._zoom
		return self._zoom_types[0] 

	def get_queryset(self, model, **kwargs):
		"""This function returns the queryset of the model specified"""
		self._queryset =  model.objects.all()
		return self._queryset

	def format_dataset(self, queryset, *args):
		""" 
		Pass a list of keys to format the dataset for your graph
		Each item in the args list is a unique field in the queryset

		ARGS:
			queryset: A django model Queryset 
			args List of fields from the queryset
		"""
		
		index = [key for key in args]
		data = {index[i]:[] for i in range(len(index))}
		for record in queryset:
			for x in range(len(index)):
				key = index[x]
				if hasattr(record, key):
					data[key].append(record.get(index[0]))

		return data
