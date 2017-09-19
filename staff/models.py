from django.db import models
from institutions.models import *
from django.utils.translation import ugettext_lazy as _

(SINGLE, MARRIED, WIDOWED, DIVORCED) = range(1, 5)
MARITAL_STATUS_CHOICES = (
    (SINGLE, _(u'Single')),
    (MARRIED, _(u'Married')),
    (WIDOWED, _(u'Widowed')),
    (DIVORCED, _(u'Divorced')),
)

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

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
        ('Mallam', 'Mallam'),
    )
    user = models.OneToOneField(User, related_name="lecturer")
    title = models.CharField(max_length=5, choices=LECTURER_TITLE, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=1, null=True, choices=SEX_CHOICES)
    marital_status = models.CharField(max_length=1, null=True, blank=True, choices=MARITAL_STATUS_CHOICES)
    email = models.EmailField(null=True)
    staff_id = models.CharField(max_length=50, blank=True)
    department = models.ForeignKey(Department, null=True)
    institution = models.ForeignKey(Institution, null=True)
    specialty = models.CharField(max_length=170, null=True, blank=True)
    position = models.ForeignKey(Position, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name = _(u'Lecturer')
        verbose_name_plural = _(u'Lecturers')
        ordering = ('first_name',)

    def __str__(self):
        return '%s %s' % (self.title, self.full_name)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)