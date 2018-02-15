from django.db import models
from institutions.models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

MARITAL_STATUS_CHOICES = (
    ('S', _(u'Single')),
    ('M', _(u'Married')),
    ('W', _(u'Widowed')),
    ('D', _(u'Divorced')),
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
    user = models.OneToOneField(User)
    title = models.CharField(max_length=20, choices=LECTURER_TITLE, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    photo = models.ImageField(upload_to="uploads/%F/%m/%d", null=True, blank=True)
    gender = models.CharField(max_length=2, null=True, choices=SEX_CHOICES)
    marital_status = models.CharField(max_length=2, null=True, blank=True, choices=MARITAL_STATUS_CHOICES)
    email = models.EmailField(null=True)
    staff_id = models.CharField(max_length=50, blank=True)
    department = models.ForeignKey(Department, null=True)
    institution = models.ForeignKey(Institution, null=True)
    specialty = models.CharField(max_length=170, null=True, blank=True)
    position = models.ForeignKey(Position, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = _(u'Lecturer')
        verbose_name_plural = _(u'Lecturers')
        ordering = ('first_name',)
        permissions = (
        	('can_edit_records', 'Staff can edit other records'),
        	('is_admin', 'Staff is an administrative user'),
        	('can_add_courses', 'Staff can add new courses'),
        	('can_add_result', 'Staff can add results')
        )

    def __str__(self):
        return '%s' % (self.full_name)

    @property
    def full_name(self):
        return "%s %s" % (self.last_name, self.first_name)

    @property
    def get_marital_status(self):
        marital_status = {'S': 'Single', 'M': 'Married', 'W': 'Widowed', 'D': 'Divorces'}
        if self.marital_status:
            return marital_status[self.marital_status]
