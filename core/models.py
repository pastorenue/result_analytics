from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import pytz

TIME_CHOICES = ((xtime, xtime) for xtime in pytz.common_timezones)

class SetupMixin(models.Model):
	user = models.OneToOneField(User)
	make_account_public = models.BooleanField(default=False)
	email_for_all_transaction = models.BooleanField(_(u'Send an email for every transaction'), default=True)
	disable_export_excel = models.BooleanField(_(u"I don't want to export excel files"), default=False)
	allow_newsletters = models.BooleanField(default=True)
	permit_collaboration = models.BooleanField(_(u'Collaborate with other staff and students'), default=True)
	time_format = models.CharField(max_length=40, choices=TIME_CHOICES, default='Africa/Lagos')
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	date_modified = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		abstract = True


class StaffSetup(SetupMixin):
	
	class Meta:
		verbose_name = _(u'Staff Setup')
		verbose_name_plural = _(u'Staffs Setup')
		ordering = ('user',)

	def __str__(self):
		return "%s's  Setup" % (self.user)


class Activation(models.Model):
	user = models.OneToOneField(User)
	accept_usage_policy = models.BooleanField(default=False)
	activated = models.BooleanField(default=False)
	manage_own_account = models.BooleanField(help_text="[Keep private (Recommended)]", default=True)
	short_motivation_quote = models.TextField(help_text="This text will be shown in your welcome page to remind of your goal", 
		blank=True)

	class Meta:
		verbose_name = _(u'Activation')
		verbose_name_plural = _(u'Activations')
		ordering = ('user',)

	def __str__(self):
		return "%s" % (self.activated)


class StudentSetup(SetupMixin):
	allow_my_result_for_analysis = models.BooleanField(default=True)
	target_cgpa = models.DecimalField(decimal_places=2, default=0.0, max_digits=4, blank=True,)
	recommed_my_help_to_students = models.BooleanField(default=True)
	recommend_me_to_students = models.BooleanField(default=True)

	def __str__(self):
		return "%s's Setup" % (self.user)

		
			