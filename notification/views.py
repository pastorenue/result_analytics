from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from notification.forms import ContactForm, SubscriptionForm
from django.shortcuts import redirect
from notification.models import Contact, Subscription


def contact(request):
    error = 'An error occured'
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact=Contact.create(name=name, email=email, message=message)
        contact.save()
        return redirect('/')
    else:
        return render(request, 'base.html',{})


# Create your views here.
