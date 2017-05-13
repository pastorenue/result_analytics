from django import forms
from courses.models import (Course, CourseRegistration, Lecturer)

class CourseForm(forms.ModelForm):
    course_code = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Course Code','class':'form-control'}))
    name = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Course Title','class':'form-control'}))
    unit = forms.CharField(widget = forms.NumberInput(attrs={'type':'number','min':'0','placeholder':'Course Credit Load','class':'form-control'}))
    

    class Meta:
        model = Course
        exclude = ['added_by',]

class CourseRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = CourseRegistration
        fields = '__all__'