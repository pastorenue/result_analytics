from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from students.forms import StudentCreationForm
from staff.forms import LecturerCreationForm
from django.db import transaction
from institutions.models import Institution

def index(request):
    context = {}
    if request.user.is_anonymous():
        return render(request, 'index.html', context)
    else:
        return HttpResponseRedirect(reverse('dashboard'))

def register_success(request):
    return render_to_response('register_success.html')

@transaction.atomic
def register_user(request):
    if request.method == 'POST':
        user_type = request.POST.get('type')
        s_form = StudentCreationForm(request.POST)
        l_form = LecturerCreationForm(request.POST)
        if l_form.is_valid() and user_type == 'staff':
            try:
                institution_id = request.POST.get('institution')
                institution = get_object_or_404(Institution, pk=institution_id)
                lecturer = l_form.save(commit=False)
                lecturer.institution = institution
                lecturer.save()
                user = authenticate(username=request.POST.get('email'), 
                        password=request.POST.get('email'))
                login(request, user)
                messages.success(request, "Welcome to Grade-X. Your WORKSPACE has \
                    been created. Ensure to change your password")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, e)
                return redirect('result_signup')

        elif s_form.is_valid() and user_type == 'student':
            try:
                institution_id = request.POST.get('institution')
                institution = get_object_or_404(Institution, pk=int(institution_id))
                student = s_form.save(commit=False)
                student.institution = institution
                student.save()
                user = authenticate(username=request.POST.get('reg_number'), 
                        password=request.POST.get('reg_number'))
                login(request, user)
                messages.success(request, "Welcome to Grade-X. Your WORKSPACE of\
                    has been successfully created. Explore the endless possibilities\
                    of academics.")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, e)
                return redirect('result_signup')
        else:
            messages.error(request, "Sorry!, your registration was not successful. \
                Perhaps you have supplied Invalid fields. If it continues please chat us up.\
                We'll be glad to help")
            return redirect('result_signup')
    else:
        s_form = StudentCreationForm()
        l_form = LecturerCreationForm()
        return render(request, 'signup.html', {'s_form': list(s_form), 'l_form': list(l_form)})
 
   
@login_required
def home(request):
    template = 'dashboard.html'

    context = {
        
    }
    return render(request, template, context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change-password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html', {
        'form': form
    })

