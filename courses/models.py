from django.db import models
from django.contrib.auth.models import User
from students.models import Student
from institutions.models import Department 
from staff.models import Lecturer
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Course(models.Model):
    SEMESTER_CHOICES = (
    (1, 'First Semester'),
    (2, 'Second Semester'),
    )
    course_code = models.CharField(max_length=7, null=True)
    name = models.CharField(max_length=250, null=True)
    unit = models.PositiveIntegerField(default=0, verbose_name="Number of credit units")
    level = models.IntegerField(choices=settings.LEVEL_CHOICES, null=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, null=True)
    department = models.ForeignKey(Department, null=True)
    lecturer = models.ManyToManyField('staff.Lecturer', help_text="Hold down the control key and select more than one lecturer",  blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    added_by = models.ForeignKey(User)
    

    class Meta:
        verbose_name = _(u'Course Available')
        verbose_name_plural = _(u'Courses Available')
        ordering = ('name',)

    def __str__(self):
        return '%s: %s' % (self.course_code, self.name)


class CourseRegistration(models.Model):
    SEMESTER_CHOICES = (
    (1, 'First Semester'),
    (2, 'Second Semester'),
    )

    student = models.ForeignKey(Student, null=True)
    level = models.PositiveIntegerField(choices=settings.LEVEL_CHOICES, null=True)
    semester = models.PositiveIntegerField(choices=SEMESTER_CHOICES, null=True)
    session = models.CharField(max_length=15, null=True)
    course = models.ManyToManyField(Course)
    carried_over = models.NullBooleanField(default=False)
    department = models.ForeignKey(Department, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = _(u'Course Registered')
        verbose_name_plural = _(u'Courses Registered')
        ordering = ('level',)

    def __str__(self):
        return self.student




# Create your models here.
