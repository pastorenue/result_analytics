from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from students.forms import StudentCreationForm
from staff.forms import LecturerCreationForm
from django.db import transaction
from institutions.models import Institution
from core.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site

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
                notify(request, lecturer.user)
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
                notify(request, student.user)
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

def notify(request, user):
    current_site = get_current_site(request)
    context_dict = {
        'name': '{0} {1}'.format(user.last_name, user.first_name),
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }
    txt_message = render_to_string('account_activation_email.txt', context_dict)
    html_message = render_to_string('account_activation_email.html', context_dict)
    subject, from_email, to = 'Grade-X: Verification Required', 'gradex.hq@gmail.com', user.email
    msg = EmailMultiAlternatives(subject, txt_message, from_email, [to])
    msg.attach_alternative(html_message, "text/html")
    try:
        msg.send()
        messages.info(request, 'Check your email for a link to activate your account.')
        return HttpResponseRedirect(reverse('account_activation_sent'))
    except:#I activate the user if I can't send email and log.
        user.is_active = True
        user.save()
        if user is not None:
            login(request, user)
        messages.success(request, 'Your account is now active')
        return HttpResponseRedirect(reverse('dashboard'))

def alternative_notify(request):
    user.is_active = True
    user.save()
    login(request, user)
    messages.success(request, 'Your account is now active')


def activation_sent(request):
    return render(request, 'account_activation_sent.html', {})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            user = User.objects.get(pk=uid)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, "Welcome to thebossoffice. Your account has been activated successfully")
            return redirect('dashboard')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Sorry! an error occured")
    return HttpResponseRedirect(reverse('dashboard'))
