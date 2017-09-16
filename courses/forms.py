from django import forms
from courses.models import (Course, CourseRegistration, Lecturer)

class CourseForm(forms.ModelForm):
    course_code = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Course Code','class':'form-control'}))
    name = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Course Title','class':'form-control'}))
    unit = forms.CharField(widget = forms.NumberInput(attrs={'type':'number','min':'0','placeholder':'Course Credit Load','class':'form-control'}))
    
    def __init__(self, *args, **kwargs):
    	super(CourseForm, self).__init__(*args, **kwargs)
    	self.fields['semester'].widget.attrs = {'class': 'form-control'}
    	self.fields['department'].widget.attrs = {'class': 'form-control'}
    	self.fields['semester'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = Course
        exclude = ['added_by',]

class CourseRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = CourseRegistration
        fields = '__all__'

class CourseCreationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CourseCreationForm, self).__init__(*args, **kwargs)
		self.fields['course_code'].widget.attrs = {'placeholder':'Course Code', 'class': 'form-control'}
		self.fields['name'].widget.attrs = {'placeholder': 'Course Title', 'class': 'form-control'}
		self.fields['unit'].widget.attrs = {'placehoder': 'Units', 'class': 'form-control'}
		self.fields['department'].widget.attrs = {'class': 'form-control'}
		self.fields['semester'].widget.attrs = {'class': 'form-control'}

	class Meta:
		model = Course
		fields = (
			'course_code',
			'name',
			'unit',
			'semester',
			'department',
		)

