
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime
from students.models import *
from django import forms
from django.db import transaction, IntegrityError
from datetime import date, timedelta
from analyzer.utils import pin_generator
#from scheduler import create_event, schedule_assignment
from states.models import Country
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget
from django.utils.text import slugify
from core.models import Activation, StudentSetup
import uuid


def create_user(email, first_name, last_name):
    """Creates a user with a username generated from the supplied `first_name` and `last_name`."""

    user = None
    user = User.objects.create(email=email, first_name=first_name, last_name=last_name)
    return user


# class ScholarshipForm(forms.ModelForm):
    
#     class Meta:
#         model = Scholarhip
#         fields = (
#             'title',
#             'provider',
#             'location',
#             'website',
#         )
        

class DocumentForm(forms.ModelForm):
    
    class Meta:
        model = Document
        fields = (
            'name',
            'attached_file',
            'description'
        )
        
        
        
class BasicProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         super(BasicProfileForm, self).__init__(*args, **kwargs)
         self.fields['email'].widget.attrs = {'placeholder' : 'Email e.g. example@example.com', 'class': 'form-control'}
         self.fields['first_name'].widget.attrs = {'placeholder' : 'Student Surname', 'class': 'form-control'}
         self.fields['last_name'].widget.attrs = {'placeholder' : 'First Name', 'class': 'form-control'}
         self.fields['middle_name'].widget.attrs = {'placeholder' : 'Other Name', 'class': 'form-control'}
         self.fields['birth_date'].widget.attrs = {'class': 'form-control'}
         self.fields['phone_number'].widget.attrs = {'class': 'form-control'}
    
    class Meta:
        model = Student
        fields = (
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'birth_date',
            'phone_number'
        )
    
    def save(self, commit=True):
        if self.instance.pk:
            user = self.instance.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        return super(BasicProfileForm, self).save(commit=commit)
    

class PersonalInformationForm(forms.ModelForm):
    """Edit an student's personal information."""
    def __init__(self, *args, **kwargs):
         super(PersonalInformationForm, self).__init__(*args, **kwargs)
         self.fields['sex'].widget.attrs = {'class': 'form-control'}
         self.fields['marital_status'].widget.attrs = {'class': 'form-control'}
         self.fields['address'].widget.attrs = {'placeholder' : 'Your location e.g #4 glo street, Ikeja ', 'class': 'form-control'}
         self.fields['state_of_residence'].widget.attrs = {'class': 'form-control'}
         self.fields['state_of_origin'].widget.attrs = {'class': 'form-control'}
         self.fields['country'].widget.attrs = {'class': 'form-control'}
         self.fields['religion'].widget.attrs = {'class': 'form-control'}
    
    class Meta:
        model = Student
        fields = (
            'sex',
            'marital_status',
            'address',
            'state_of_residence',
            'state_of_origin',
            'country',
            'religion',
        )    


class SchoolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         super(SchoolForm, self).__init__(*args, **kwargs)
         self.fields['reg_number'].widget.attrs = {'placeholder' : 'Reg Number', 'class': 'form-control'}
         self.fields['institution'].widget.attrs = {'class': 'form-control'}
         self.fields['library_id_number'].widget.attrs = {'placeholder' : 'Enter Library Id', 'class': 'form-control'}
         self.fields['program_type'].widget.attrs = {'class': 'form-control'}
         self.fields['department'].widget.attrs = {'class': 'form-control'}
         self.fields['faculty'].widget.attrs = {'class': 'form-control'}
         self.fields['year_of_admission'].widget.attrs = {'class': 'form-control'}
         self.fields['level'].widget.attrs = {'class': 'form-control'}
         self.fields['course_duration'].widget.attrs = {'max_length': 1, 'class': 'form-control'}

    
    class Meta:
        model = Student
        fields = (
            'reg_number',
            'institution',
            'library_id_number',
            'program_type',
            'department',
            'faculty',
            'year_of_admission',
            'level',
            'course_duration'
        )
        
class BankForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = (
            'bank',
            'bank_account_number',
        )


class StudentCreationForm(forms.ModelForm):
    year_of_admission = forms.DateField(widget = SelectDateWidget(years=range(1990, datetime.date.today().year+50), attrs=({'class': 'form-control', 'style': 'width: 30%; display: inline-block;'})))

    def __init__(self, *args, **kwargs):
         super(StudentCreationForm, self).__init__(*args, **kwargs)
         self.fields['email'].widget.attrs = {'placeholder' : 'Email e.g. example@example.com', 'class': 'form-control'}
         self.fields['last_name'].widget.attrs = {'placeholder' : 'Student Surname', 'class': 'form-control'}
         self.fields['first_name'].widget.attrs = {'placeholder' : 'First Name', 'class': 'form-control'}
         self.fields['middle_name'].widget.attrs = {'placeholder' : 'Other Name', 'class': 'form-control'}
         self.fields['reg_number'].widget.attrs = {'placeholder' : 'Reg Number', 'class': 'form-control'}
         self.fields['faculty'].widget.attrs = {'class': 'form-control'}
         self.fields['department'].widget.attrs = {'class': 'form-control'}
         self.fields['level'].widget.attrs = {'class': 'form-control'}
         self.fields['course_duration'].widget.attrs = {'max_length': 1, 'class': 'form-control'}

    class Meta:
        model = Student
        fields = (
            'email',
            'last_name',
            'first_name',
            'middle_name',
            'reg_number',
            'faculty',
            'department',
            'level',
            'year_of_admission',
            'course_duration'
        )

 
    @transaction.atomic
    def save(self, commit=True):
        user = create_user(self.cleaned_data['email'], self.cleaned_data['last_name'], self.cleaned_data['first_name'])
        # Set default password to this user's username and birth date (if provided):
        # password = pin_generator()
        user.username = self.cleaned_data['reg_number']
        user.set_password(self.cleaned_data['reg_number'])
        user.save()

        setup = StudentSetup(user=user)
        setup.save()

        activation = Activation(user=user)
        activation.save()

        instance = super(StudentCreationForm, self).save(commit=False)
        instance.user = user
        orig = slugify(instance.last_name)
        if Student.objects.filter(slug=instance.slug).exists():
            instance.slug = "%s-%s" % (orig, uuid.uuid4())
        else:
            instance.slug = "%s-%s" % (orig, uuid.uuid4())

        instance.save()
        return instance


class ScholarshipForm(forms.ModelForm):

    class Meta:
        model = Scholarship
        fields = {
            'title',
            'provider',
            'location',
        }