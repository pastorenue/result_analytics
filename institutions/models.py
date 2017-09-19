from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import uuid

class Institution(models.Model):
    name = models.CharField(max_length=250, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    logo = models.ImageField(upload_to='institution/logo/%Y/%m/', blank=True)
    postal_code = models.CharField(max_length=30, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)
    #grading_type = models.OneToOneField(Grade)

    class Meta:
        verbose_name = _(u'Institution')
        verbose_name_plural = _(u'Institutions')
        ordering = ('name',)

    def __str__(self):
        return '%s, %s' % (self.name, self.location)


class Faculty(models.Model):
    code = models.CharField(max_length=5, null=True)
    name = models.CharField(max_length=250, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Faculty')
        verbose_name_plural = _(u'Faculties')

    def __str__(self):
        return self.name

class Department(models.Model):
    code = models.CharField(max_length=3, null=True)
    id_number = models.IntegerField(blank=True, null=True)
    faculty = models.ForeignKey(Faculty, related_name='department', null=True)
    name = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Department')
        verbose_name_plural = _(u'Departments')

    def __str__(self):
        return self.name
    
class DepartmentalCode(models.Model):
    name = models.CharField(max_length=50, null=True)
    code = models.IntegerField(null=True)
    
    def __str__(self):
        return '%s: %s' % (self.name, self.code)
    
    class Meta:
        verbose_name = _(u'Departmental Code')
        verbose_name_plural = _(u'Departmental Codes')
        ordering = ('name',)

class AcadamicYear(models.Model):
    year_starting = models.DateField()
    year_ending = models.DateField()

    def __str__(self):
        return "from %s to %s" % (self.year_starting, self.year_ending)

class AdminStaff(models.Model):
    user = models.OneToOneField(User)
    institution = models.OneToOneField(Institution)
    