from .models import Lecturer
from django import forms
from django.contrib.auth.models import User
from analyzer.utils import pin_generator
from core.models import Activation, Setup

class LecturerForm(forms.ModelForm):

	class Meta:
		model = Lecturer
		fields = (
			'title',
			'first_name',
			'last_name',
			'email',
			'faculty',
			'department',
			'specialty',
			'position'
		)

	def save(self):
		user = User(first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], email=self.cleaned_data['email'])
		user_name = last_name+pin_generator(length=4)
		password = pin_generator(length=8)
		user.user_name = user_name
		user.set_password = password
		user.save()

		activation = Activation(user=user)
		activation.save()

		setup = Setup(user=user)
		setup.save()

		instance = super(LecturerForm, self).save(commit=False)
		instance.user = user_name

		orig = slugify(instance.last_name)
        if Student.objects.filter(slug=instance.slug).exists():
            instance.slug = "%s-%s" % (orig, instance.unique_id)
        else:
            instance.slug = "%s-%s" % (orig, instance.unique_id)
        instance.save()
        return instance


class FacultyForm(forms.ModelForm):

	class Meta:
		model = Faculty
		fields = '__all__'

class DepartmentForm(forms.ModelForm):

	class Meta:
		model = Department
		fields = '__all__'

