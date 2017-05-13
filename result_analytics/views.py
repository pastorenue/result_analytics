from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from notification.forms import ContactForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/#contact')
    else:
        form = ContactForm()
    context = {'form':form}
    return render(request, 'base.html', context)

def register_success(request):
    return render_to_response('register_success.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password1')
        user=User.objects.create_user(username=username, password=password, first_name = firstname, last_name=lastname)
        user.save()
        profile = Profile(user=user, first_name=firstname, last_name=lastname)
        profile.save()
        return redirect('photobox_success')
    else:
        return render(request, 'signup.html', {})
 
   
@login_required
def home(request):
    if request.user.is_active:
        tag = "Active User"
    else:
        tag = "%s" % (request.user)
    if not request.user.is_authenticated():
        return redirect('login.html')
    else:
        photos = Photo.objects.filter(user = request.user)
        return render(request, template, context)