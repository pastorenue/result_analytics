from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from students.forms import StudentCreationForm

def index(request):
    context = {}
    if request.user.is_anonymous():
        return render(request, 'index.html', context)
    else:
        return HttpResponseRedirect(reverse('dashboard'))

def register_success(request):
    return render_to_response('register_success.html')

def register_user(request):
    if request.method == 'POST':
        s_form = StudentCreationForm(request.POST, request.FILES)
        if s_form.is_valid:
            s_form.save()
        return redirect('photobox_success')
    else:
        s_form = StudentCreationForm()
        return render(request, 'signup.html', {'s_form': list(s_form)})
 
   
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

