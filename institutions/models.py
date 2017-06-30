from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
class Institution(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)

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


class Position(models.Model):
    """
    The position the lecturer  occupies within the institution.
    """
    reports_to = models.ForeignKey('self', null=True, blank=True, related_name='reports')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _(u'Position')
        verbose_name_plural = _(u'Positions')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Lecturer(models.Model):
    '''brief detail of Lecturers information'''

    LECTURER_TITLE = (
    ('Mr.', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Dr.', 'Dr'),
    ('Prof', 'Prof'),
    ('Prof', 'Mallam'),
)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=5, choices=LECTURER_TITLE, null=True, blank=True)
    name = models.CharField(max_length=250, null=True)
    department = models.ForeignKey(Department, null=True)
    specialty = models.CharField(max_length=170, null=True, blank=True)
    position = models.ForeignKey(Position, null=True, blank=True)

    class Meta:
        verbose_name = _(u'Lecturer')
        verbose_name_plural = _(u'Lecturers')
        ordering = ('name',)

    def __str__(self):
        return '%s %s' % (self.title, self.name)


class InstitutionDetail(models.Model):
    '''
    Gives the complete detail of the institution. Will be relevant when schools wan to have specific control.
    It might be useful in the future
    '''
    institution = models.ForeignKey(Institution, null=True)
    logo = models.ImageField(upload_to='institution/logo/%Y/%m/', blank=True)
    postal_code = models.CharField(max_length=30, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _(u'Institution Complete Detail')
        verbose_name_plural = _(u'Institution Complete Details')
        ordering = ('institution',)

    def __str__(self):
        return self.institution
    
class DeparmentalCode(models.Model):
    name = models.CharField(max_length=50, null=True)
    code = models.IntegerField(null=True)
    
    def __str__(self):
        return '%s: %s' % (self.name, self.code)
    
    class Meta:
        verbose_name = _(u'Departmental Code')
        verbose_name_plural = _(u'Departmental Codes')
        ordering = ('name',)