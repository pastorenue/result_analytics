from django.contrib.auth.models import User
from django.utils.timezone import now
from students.models import *
from django import forms
from form_utils.widgets import CalendarWidget, DateFieldMixin
from django.db import transaction, IntegrityError
from datetime import date, timedelta
from form_utils.base import ModelForm
#from scheduler import create_event, schedule_assignment
from states.models import Country



def create_user(first_name, last_name):
    """Creates a user with a username generated from the supplied `first_name` and `last_name`."""
    user = None
    for i in range(len(first_name)):
        username = ("%s%s" % (first_name[:i+1], last_name)).lower()
        if(User.objects.filter(username=username)):
            continue#username exists, try next
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name)
        break
    else:
        for i in xrange(100):
            if(User.objects.filter(username=username)):
                continue
            user = User.objects.create(username="%s%d" % (username, i))
            break
        else:
            # Should probably add some code here to handle the case where a username can't
            # be generated (should that ever happen):
            raise Exception(u'No available username for: %s %s' % (first_name, last_name))
    return user

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'file',
            'tag',
        )
        

class ScholarshipForm(forms.ModelForm):
    
    class Meta:
        model = Scholarhip
        fields = (
            'title',
            'provider',
            'location',
            'website',
        )
        

class DocumentForm(forms.ModelForm):
    
    class Meta:
        model = Document
        fields = (
            'file','description'
        )
        
        
        
class BasicProfileForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = (
            'title',
            'first_name',
            'last_name',
            'middle_name',
            'photo',
            'birth_date',
            'unit',
            'position',
            'email',
            'phone',
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
    
    class Meta:
        model = Student
        fields = (
            'sex',
            'genotype',
            'blood_group',
            'marital_status',
            'address',
            'permanent_address',
            'state_of_residence',
            'state_of_origin',
            'lga',
            'country',
            'national_id_number',
            'religion',
        )

    def __init__(self, *args, **kwargs):
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        self.fields['lga'].widget.attrs['class'] = 'chainedSelect { parent: "#id_state_of_origin", url: "%s" }' % (reverse('states_lga_by_state'))
        if 'country' not in self.initial:
            try:
                self.initial['country'] = Country.objects.get(code='NGA').pk # 9ja 4 life :)
            except Country.DoesNotExist:
                pass


class SchoolForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = (
            'reg_number'
            'student_institution',
            'library_id_number',
            'program_type',
            'department',
            'faculty',
            'year_of_graduation',
        )
        
class BankForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = (
            'bank',
            'bank_account_number',
        )


class StudentCreationForm(DateFieldMixin, ModelForm):
    """A (much) simpler form, containing only the required fields for creating an employee."""

    class Meta:
        model = Employee
        widgets = {
            'birth_date': CalendarWidget(year_range=(-60, 1)),
            'hire_date': CalendarWidget(year_range=(-60, 1)),
            'sex': widgets.RadioSelect,
        }
        fields = (
            'staff_id_number',
            'first_name',
            'last_name',
            'email',
            'employee_type',
            'birth_date',
            'sex',
            'position',
            'location',
            'grade_level',
            'basic',
            'pay_template',
            'unit',
            'state_of_origin',
            'state_of_residence',
            'hire_date',
        )

    def __init__(self, *args, **kwargs):
        super(StudentCreationForm, self).__init__(*args, **kwargs)
        self.initial.update({
            'hire_date': date.today(),
        })

    @transaction.atomic
    def save(self, commit=True):
        user = create_user(self.cleaned_data['first_name'], self.cleaned_data['last_name'])
        user.email = self.cleaned_data['email']
        # Set default password to this user's username and birth date (if provided):
        suffix = self.cleaned_data['birth_date'].strftime('%Y%m%d') if self.cleaned_data['birth_date'] else ''
        user.set_password(user.username + suffix)
        user.save()

        student = super(StudentCreationForm, self).save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student
