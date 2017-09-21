from django import forms
from .models import StaffSetup, StudentSetup, Activation

class StaffSetupForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(StaffSetupForm, self).__init__(*args, **kwargs)
		self.fields['time_format'].widget.attrs = {'class': 'form-control'}

	class Meta:
		model = StaffSetup
		exclude = ('user',) 

class StudentSetupForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(StudentSetupForm, self).__init__(*args, **kwargs)
		self.fields['time_format'].widget.attrs = {'class': 'form-control'}
		self.fields['target_cgpa'].widget.attrs = {'class': 'form-control', 'step': '0.1'}

	class Meta:
		model = StudentSetup
		exclude = ('user',)

class ActivationForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ActivationForm, self).__init__(*args, **kwargs)
		self.fields['short_motivation_quote'].widget.attrs = {'class': 'form-control'}
	
	class Meta:
		model = Activation
		exclude = ('user', 'activated')
