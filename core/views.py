from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import StaffSetupForm, StudentSetupForm, ActivationForm
from django.contrib.auth.decorators import login_required
from .models import StaffSetup, StudentSetup, Activation
from django.contrib import messages
from students.models import Student
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
# Create your views here.

@login_required
def setup(request):
	form = []
	student_setup = None
	staff_setup = None
	if hasattr(request.user, 'student'):
		student_setup = StudentSetup.objects.get(user=request.user)
	if hasattr(request.user, 'lecturer'):
		staff_setup = StaffSetup.objects.get(user=request.user)
	if request.method == 'POST':
		request.session['django_timezone'] = request.POST.get('time_format')
		if hasattr(request.user, 'lecturer'):
			form = StaffSetupForm(request.POST, instance=staff_setup)
			form.save()
			messages.success(request, "Your configuration has been saved")
			return redirect('dashboard')
		elif hasattr(request.user, 'student'):
			form = StudentSetupForm(request.POST, instance=student_setup)
			form.save()
			messages.success(request, "Your configuration has been saved")
			return redirect('dashboard')
	else: 
		if hasattr(request.user, 'lecturer'):
			form = StaffSetupForm(instance=staff_setup)
		elif hasattr(request.user, 'student'):
			form = StudentSetupForm(instance=student_setup)
	return render(request, 'setup.html', {'form': list(form)})


@login_required
def activate(request):
	template_name = 'core/activate.html'
	instance = get_object_or_404(Activation, user=request.user)
	if request.method == 'POST':
		form = ActivationForm(request.POST, instance=instance)
		if form.is_valid():
			try:
				form = form.save(commit=False)
				form.activated = True
				form.user = request.user
				form.save()
				messages.info(request, "Your account has been activated. \
					Enjoy the full features of Grade-X")
				return redirect('dashboard')
			except Exception as e:
				messages.error(request, e) 
	else:
		form = ActivationForm(instance=instance)
	return render(request, template_name, {'form': list(form)})

@login_required
def update_quote(request):
	if request.method =="POST":
		quote = request.POST.get("quote")
		activation = get_object_or_404(Activation, user=request.user)
		activation.short_motivation_quote = quote
		activation.save()
		messages.success(request, "Your Quote has been Updated!")
		return redirect('user-settings') 

def check_user(request):
	message = ""
	if request.method == "POST":
		reg_number = request.POST.get('check')
		if Student.objects.filter(reg_number=reg_number).exists():
			message = "The Reg Number: '%s' was Found" % (reg_number)
			messages.info(request, message)
		else:
			message = "Sorry! The Reg Number: '%s' was not Found" % (reg_number)
			messages.info(request, message)
		return HttpResponseRedirect(reverse('result_login'))