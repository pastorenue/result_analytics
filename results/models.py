from django.db import models
from django.utils.translation import ugettext_lazy as _
from courses.models import Course
from django.conf import settings
from decimal import Decimal
from django.db.models import Sum
from students.models import Student
from institutions.models import Department, Institution
from functools import reduce

def decimal_add(x, y):
    '''
    This is an operator for a decimal addition. 
    '''
    return Decimal(x) + Decimal(y)

class Grading(models.Model):
    institution = models.ForeignKey(Institution, null=True)
    caption = models.CharField(max_length=15, null=True)
    grade_points = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    start = models.IntegerField(null=True, default=0)
    end = models.PositiveIntegerField(null=True, default=100)

    class Meta:
        verbose_name = _(u'Grading')
        verbose_name_plural = _(u'Gradings')
        ordering = ('caption',)

    def __str__(self):
        return self.caption

class ResultManager(models.Manager):

    def get_staff_results(self, request):
        return self.filter(course__lecturers=request.user.lecturer)


class Result(models.Model):
    student = models.ForeignKey(Student, null=True)
    course = models.ForeignKey(Course, null=True)
    exam_score = models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6)
    assignment_score = models.DecimalField(null=True,  default=0.0, decimal_places=2, max_digits=6)
    quiz_score = models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6)
    total_score = models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6)
    level = models.PositiveIntegerField(choices=settings.LEVEL_CHOICES,null=True, blank=True)
    semester = models.PositiveIntegerField(choices=settings.SEMESTER_CHOICES, null=True)
    department = models.ForeignKey(Department, null=True, blank=True)
    institution = models.ForeignKey(Institution, null=True)
    credit_load = models.DecimalField(default=0.0, decimal_places=2, max_digits=4, blank=True, null=True)
    session = models.CharField(max_length=10, blank=True, null=True)
    course_load = models.DecimalField(default=0.0, decimal_places=2, max_digits=4, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    objects = ResultManager()

    class Meta:
        verbose_name = _(u'Student Result')
        verbose_name_plural = _(u' Student Results')
        ordering = ('-date_created',)
        
    def __str__(self):
        return '%s' % (self.total_score)
    
    def save(self, **kwargs):
        self.credit_load = self.get_credit_load
        self.course_load = self.get_course_load
        self.department = self.student.department
        self.total_score = self.get_total_score()
        
        super(Result, self).save(**kwargs)

    @property
    def grade(self):
        score = self.get_total_score()
        grades = Grading.objects.filter(institution=self.student.institution)
        grade = [grade.caption for grade in grades if score in range(grade.start, grade.end+1)]
        
        return grade[0]
    
    def get_total_score(self):
        total = reduce(decimal_add, [self.exam_score,self.assignment_score, self.quiz_score, 0.0])
        return total

    @property
    def grade_points(self):
        grade = self.grade
        grading = Grading.objects.get(institution=self.student.institution, caption=grade)
        return grading.grade_points
    
    @property
    def get_credit_load(self):
        return self.course.unit
    
    @property
    def get_course_load(self):
        course_load = Decimal((self.course.unit*self.grade_points))
        return course_load


class CGPA(models.Model):
    student = models.ForeignKey(Student)
    cgpa = models.DecimalField(verbose_name='student_cgpa', max_digits=3,decimal_places=2)
    semester = models.PositiveIntegerField(choices=settings.SEMESTER_CHOICES, null=True)
    level = models.PositiveIntegerField(null=True)
    session = models.CharField(max_length=15)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s for semester %s %s session' % (self.cgpa, self.semester, self.session)

    class Meta:
        verbose_name = _(u'CGPA')
        verbose_name_plural = _(u'CGPAs')
        ordering = ('-date_created',)
        
