from django.db import models
from django.utils.translation import ugettext_lazy as _
from institutions.models import Department
from results.models import Result

class Actvity(models.Model):
    activity_name = models.CharField(max_length=100, null=True)
    department = models.ForeignKey(Department)
    results = models.ForeignKey(Result)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _(u'Analysis Activity')
        verbose_name_plural = _(u'Analysis Activities')
        ordering = ('date_created',)
        
    def __str__(self):
        return self.activity_name

# Create your models here.
