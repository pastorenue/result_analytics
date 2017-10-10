from django import forms
from .models import Lecturer
from django.db import transaction
import uuid
from django.contrib.auth.models import User
from core.models import *
from django.utils.text import slugify

def create_user(email, first_name, last_name):
    """Creates a user with a username generated from the supplied `first_name` and `last_name`."""

    user = None
    user = User.objects.create(email=email, first_name=first_name, last_name=last_name)
    return user


class LecturerCreationForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(LecturerCreationForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs = {'placeholder': 'valid email address. e.g example@example.com', 'class': 'form-control'}
		self.fields['first_name'].widget.attrs = {'placeholder':'First Name', 'class': 'form-control'}
		self.fields['last_name'].widget.attrs = {'placeholder':'Last Name', 'class': 'form-control'}
		self.fields['gender'].widget.attrs = {'class': 'form-control'}
		self.fields['marital_status'].widget.attrs = {'class': 'form-control'}
		self.fields['staff_id'].widget.attrs = {'placeholder': '[optional] Staff ID number', 'class': 'form-control'}
		self.fields['department'].widget.attrs = {'class': 'form-control'}
	
	class Meta:
		model = Lecturer
		fields = (
			'email',
			'first_name',
			'last_name',
			'gender',
			'marital_status',
			'staff_id',
			'department',
		)

	@transaction.atomic
	def save(self, commit=True):
	    user = create_user(self.cleaned_data['email'], self.cleaned_data['last_name'], self.cleaned_data['first_name'])
	    # Set default password to this user's username and birth date (if provided):
	    # password = pin_generator()
	    user.username = self.cleaned_data['email']
	    user.set_password(self.cleaned_data['email'])
	    user.is_staff = True
	    user.save()

	    setup = StaffSetup(user=user)
	    setup.save()

	    activation = Activation(user=user)
	    activation.save()

	    instance = super(LecturerCreationForm, self).save(commit=False)
	    instance.user = user
	    orig = slugify(instance.last_name)
	    if Lecturer.objects.filter(slug=instance.slug).exists():
	        instance.slug = "%s-%s" % (orig, uuid.uuid4())
	    else:
	        instance.slug = "%s-%s" % (orig, uuid.uuid4())

	    instance.save()
	    return instance


class CustomStaffCreationForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(CustomStaffCreationForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs = {'placeholder': 'valid email address. e.g example@example.com', 'class': 'form-control'}
		self.fields['first_name'].widget.attrs = {'placeholder':'First Name', 'class': 'form-control'}
		self.fields['last_name'].widget.attrs = {'placeholder':'Last Name', 'class': 'form-control'}
		self.fields['gender'].widget.attrs = {'class': 'form-control'}
		self.fields['marital_status'].widget.attrs = {'class': 'form-control'}
		self.fields['staff_id'].widget.attrs = {'placeholder': '[optional] Staff ID number', 'class': 'form-control'}
		self.fields['department'].widget.attrs = {'class': 'form-control'}
	
	class Meta:
		model = Lecturer
		fields = (
			'email',
			'first_name',
			'last_name',
			'gender',
			'marital_status',
			'staff_id',
			'department'
		)

	@transaction.atomic
	def save(self, commit=True):
	    user = create_user(self.cleaned_data['email'], self.cleaned_data['last_name'], self.cleaned_data['first_name'])
	    # Set default password to this user's username and birth date (if provided):
	    # password = pin_generator()
	    user.username = self.cleaned_data['email']
	    user.set_password(self.cleaned_data['email'])
	    user.is_staff = True
	    user.save()

	    setup = StaffSetup(user=user)
	    setup.save()

	    activation = Activation(user=user)
	    activation.save()

	    instance = super(CustomStaffCreationForm, self).save(commit=False)
	    instance.user = user
	    orig = slugify(instance.last_name)
	    if Lecturer.objects.filter(slug=instance.slug).exists():
	        instance.slug = "%s-%s" % (orig, uuid.uuid4())
	    else:
	        instance.slug = "%s-%s" % (orig, uuid.uuid4())

	    instance.save()
	    return instance