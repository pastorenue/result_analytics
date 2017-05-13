__author__ = 'admin'
from django import forms
from notification.models import Contact, Subscription

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = '__all__'
