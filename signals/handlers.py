from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from notifications.signals import notify
from django.contrib.auth.models import User


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='has been sent to you')

post_save.connect(my_handler, sender=User)
