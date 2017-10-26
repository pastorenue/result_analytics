# add assignent form code here
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from .models import Assignment, AssignmentScore, Submitted
import datetime
from students.models import Student
from django.db import transaction
from courses.models import Course

class AssignmentForm(forms.ModelForm):
	due_date = forms.DateTimeField(widget = SelectDateWidget(years=range(1990, datetime.date.today().year+20), attrs=({'class': 'form-control', 'style': 'width: 30%; display: inline-block; text-align: left;'})))
	
	class Meta:
		model = Assignment
		exclude = ('lecturer','status')

	def __init__(self, request, *args, **kwargs):
		#self.request = kwargs.pop('request')
		super(AssignmentForm, self).__init__(*args, **kwargs)
		self.fields['course'].widget.attrs = {'class':'form-control'}
		self.fields['course'].queryset = Course.objects.filter(lecturers=request.user.lecturer)
		self.fields['possible_points'].widget.attrs = {'class':'form-control'}
		self.fields['question_or_instructions'].widget.attrs = {'class': 'form-control', 'rows': '3', 'placeholder':'Enter a question or description of the attached if any'}
		self.fields['level'].widget.attrs = {'class':'form-control'}
		self.fields['category'].widget.attrs = {'class':'form-control'}
		self.fields['standard'].widget.attrs = {'class':'form-control'}
		self.fields['semester'].widget.attrs = {'class': 'form-control'}
		self.fields['session'].widget.attrs = {'class':'form-control'}

	@transaction.atomic
	def save(self, commit=False):
		instance = super(AssignmentForm, self).save(commit=False)
		instance.lecturer = self.request.user.lecturer
		instance.save()
		students = Student.objects.filter(institution=self.request.user.lecturer.institution)
		assignment_objects = []

		for student in students:
			if student.level == instance.level:
				tmp_record = AssignmentScore(student=student, assignment=instance)
				assignment_objects.append(tmp_record)
			else:
				continue

		AssignmentScore.objects.bulk_create(assignment_objects)

		
		return instance


class AssignmentSubmitForm(forms.ModelForm):

	class Meta:
		model = Submitted
		exclude = ('student', 'assignment')

	def __init__(self, *args, **kwargs):
		super(AssignmentSubmitForm, self).__init__(*args, **kwargs)
		self.fields['answer'].widget.attrs = {'class':'form-control'}
