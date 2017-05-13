from django import forms
from django.contrib.auth.models import User
from django.contrib.admin import widgets as admin_widgets
from django.core.urlresolvers import reverse
from django.db import transaction, IntegrityError
from django.forms import fields, widgets, models
from django.utils.timezone import now
from configstore.configs import get_config
from employees.models import *
from form_utils.base import ModelForm
from form_utils.widgets import CalendarWidget, DateFieldMixin
from scheduler import create_event, schedule_birthday
from states.models import Country
from datetime import date, timedelta
from itertools import chain
import os

employee_options = get_config('employee_options')

def id_generator(width=8):
    """
    Generates a sequential fixed-width number.

    Each time this function is called, it counts the number of employees in the employee
    table, adds 1 to that value, and returns it, formatted as a fixed-width string.

    Not quite sure why we do this right now...maybe it'll become clearer sometime soon.
    """
    num = Employee.objects.aggregate(num=models.Count('pk'))['num'] or 0
    return str(num + 1).zfill(width)

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

class EmployeeCreationForm(DateFieldMixin, ModelForm):
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
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)
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

        employee = super(EmployeeCreationForm, self).save(commit=False)
        if not employee.staff_id_number:
            employee.staff_id_number = id_generator()
        employee.user = user
        if commit:
            employee.save()

        # Schedule confirmation and birthday:
        if employee.birth_date:
            schedule_birthday(employee)
        hr = [e.user for e in employee_options['hr_group'].get_queryset()]
        create_event(
            employee,
            "%s's Confirmation" % employee.full_name,
            ('CONF', 'Employee Confirmations'),
            start_time=(now() + timedelta(weeks=employee_options['probation_period'])),
            users=chain([employee.user], hr)
        )
        return employee

class BasicProfileForm(DateFieldMixin, ModelForm):
    """Edit an employee's basic profile information."""

    class Meta:
        model = Employee
        widgets = {
            'photo': admin_widgets.AdminFileWidget,
            'birth_date': CalendarWidget(year_range=(-60, 1)),
        }
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

class CompanyInformationForm(DateFieldMixin, ModelForm):
    """Edit an employee's company-related information."""
    
    class Meta:
        model = Employee
        fields = (
            #'status',  # TODO: implement "confirm", "retire", "resign" and "dismiss" actions.
            #'confirmation_date',   # TODO: set when employee is confirmed (see above).
            #'termination_date',    # TODO: set when employee is terminated (see above).
            'location',
            'bank',
            'bank_account_number',
            'pension_administrator',
            'pfa_pin',
            'tax_id',
        )

class PersonalInformationForm(DateFieldMixin, ModelForm):
    """Edit an employee's personal information."""
    
    class Meta:
        model = Employee
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
            'passport_number',
            'national_id_number',
            'religion',
            'maiden_name',
            'mothers_maiden_name',
        )

    def __init__(self, *args, **kwargs):
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        self.fields['lga'].widget.attrs['class'] = 'chainedSelect { parent: "#id_state_of_origin", url: "%s" }' % (reverse('states_lga_by_state'))
        if 'country' not in self.initial:
            try:
                self.initial['country'] = Country.objects.get(code='NGA').pk # 9ja 4 life :)
            except Country.DoesNotExist:
                pass

class NextOfKinForm(DateFieldMixin, ModelForm):
    class Meta:
        model = NextOfKin
        exclude = ('employee',)

class DependentForm(DateFieldMixin, ModelForm):
    class Meta:
        model = Dependent
        exclude = ('employee',)
        widgets = {
            'birth_date': CalendarWidget(year_range=(-100, 1)),
        }

class EducationForm(DateFieldMixin, ModelForm):
    class Meta:
        model = Education
        exclude = ('employee',)
        widgets = {
            'start_date': CalendarWidget(year_range=(-50, 1)),
            'end_date': CalendarWidget(year_range=(-50, 1)),
        }

class ExperienceForm(DateFieldMixin, ModelForm):
    class Meta:
        model = Experience
        exclude = ('employee',)
        widgets = {
            'start_date': CalendarWidget(year_range=(-50, 1)),
            'end_date': CalendarWidget(year_range=(-50, 1)),
        }

class PlacementForm(DateFieldMixin, ModelForm):
    class Meta:
        model = Placement
        exclude = ('employee',)

    def __init__(self, *args, **kwargs):
        employee = kwargs.pop('employee')
        super(PlacementForm, self).__init__(*args, **kwargs)
        if employee:
            self.employee = employee
            self.initial = {
                'position': employee.position.pk,
                'location': employee.location.pk,
                'unit': employee.unit.pk,
            }

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('file', 'description',)

    def save(self, commit=True):
        file = self.cleaned_data['file']
        name, ext = os.path.splitext(os.path.basename(file.name))
        doc = Document(name=name, description=self.cleaned_data['description'])
        # We'll use our UID as the filename:
        doc.file.save(doc.uid + ext, file, False)
        if commit:
            doc.save()
        return doc

class ExitForm(DateFieldMixin, ModelForm):
    class Meta:
        model = Termination
        exclude = ('employee', 'user',)

class LifeInsuranceForm(DateFieldMixin, ModelForm):
    class Meta:
        model = LifeInsurance
        exclude = ('employee',)
        widgets = {
            'start_date': CalendarWidget(year_range=(-15, 5)),
            'end_date': CalendarWidget(year_range=(-5, 25)),
        }

class IncidenceForm(DateFieldMixin, ModelForm):
    class Meta:
        model = Incidence
        exclude = ('employee',)
