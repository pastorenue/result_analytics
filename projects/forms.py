from .models import *
from django import forms
from staff.models import Lecturer


class ProjectForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProjectForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs = {'class':'form-control'}
		self.fields['description'].widget.attrs = {'class':'form-control'}
		self.fields['file'].widget.attrs = {'class':'form-control'}
		self.fields['tag'].widget.attrs = {'class':'form-control'}
		self.fields['supervisor'].widget.attrs = {'class':'form-control'}
	    
	class Meta:
	    model = Project
	    fields = (
	        'name',
	        'description',
	        'file',
	        'tag',
	        'supervisor'
	    )
	    
