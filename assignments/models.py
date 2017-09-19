from django.db import models, transaction
from courses.models import Course
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from students.models import Student
from institutions.models import Institution 
from staff.models import Lecturer
import uuid
# Create your models here.

class Assignment(models.Model):
	EXCELLENT, ABOVE_AVERAGE, AVERAGE, FAIR_ENOUGH = (80, 60, 50, 40)
	ASSIGNMENT_STANDARD = (
        (EXCELLENT, 'Excellence'),
        (ABOVE_AVERAGE, 'Above Average'),
        (AVERAGE, 'Average'),
        (FAIR_ENOUGH, 'Fair Enough')
    )
	ASSIGNMENT_TYPE = (
        ('quiz', 'Quiz'),
        ('major assignment', 'Major Assignments'),
        ('mock assignment', 'Mock Assignment')
    )
	
	lecturer = models.ForeignKey(Lecturer, null=True)
	assignment_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	course = models.ForeignKey(Course, null=True)
	question_or_instructions = models.TextField()
	level = models.PositiveIntegerField(choices=settings.LEVEL_CHOICES, null=True)
	file = models.FileField(upload_to='uploads/assigments/%Y/%m/%d/', blank=True)
	category = models.CharField(max_length=20, choices=ASSIGNMENT_TYPE, default='mock assignment', blank=True)
	standard = models.PositiveIntegerField(choices=ASSIGNMENT_STANDARD, default=50, blank=True)
	semester = models.PositiveIntegerField(choices=settings.SEMESTER_CHOICES, null=True)
	session = models.CharField(max_length=10, blank=True, null=True)
	possible_points = models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	due_date = models.DateTimeField()

	def __str__(self):
		return "%s" % (self.question_or_instructions[:20])

	class Meta:
		ordering = ('-created',)


class AssignmentScore(models.Model):
 
    ASSIGNMENT_STATUS = (
		('A', 'Active'),
		('D', 'Declined'),
		('S', 'Submitted'),
		('M', "Marked")
	)
    student = models.ForeignKey(Student, null=True)
    assignment = models.ForeignKey(Assignment)
    status = models.CharField(max_length=1, choices=ASSIGNMENT_STATUS, default='A')
    score = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _(u'Assigment Grade')
        verbose_name_plural = _(u'Assignment Grades')
        ordering = ('-date_created',)
    
    @transaction.atomic
    def save(self, **kwargs):
    	result = Result.objects.filter(student=self.student, course=self.assignment.course, 
    			semester=self.assignment.semester)
    	if result.exists():
    		if result[0].assignment_score == 0.0:
    			result[0].assignment_score = self.score
    			result[0].save()
    		else:
    			pass
    	super(Assignment, self).save(**kwargs)


class Quiz(models.Model):
	student = models.ForeignKey(Student)
	score = models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6)
	course = models.ForeignKey(Course)
	level = models.PositiveIntegerField(choices=settings.LEVEL_CHOICES, null=True, blank=True)
	semester = models.PositiveIntegerField(choices=settings.SEMESTER_CHOICES, null=True)
	session = models.CharField(max_length=10, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	invigilators = models.ManyToManyField('staff.Lecturer', help_text="Hold down the control key and select more than one lecturer",  blank=True)

	class Meta:
		verbose_name = _(u'Quiz')
		verbose_name_plural = _(u'Quizes')
		ordering = ('-date_created',)

	def __str__(self):
		return "%s: %s" % (self.student, self.score)

	@transaction.atomic
	def save(self, **kwargs):
		result = Result.objects.filter(student=self.student, course=self.assignment.course, 
    			semester=self.assignment.smester)
		if result.exists():
			if result[0].quiz_score != 0.0:
				result[0].quiz_score = self.score
				result[0].save()
			else:
				pass
		super(Quiz, self).save(**kwargs)


class Submitted(models.Model):
	student = models.ForeignKey(Student)
	answer = models.TextField()
	assignment = models.ForeignKey(Assignment)
	upload_file = models.FileField(upload_to="uploads/assignment_answers/%Y/%m/%d", blank=True)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _(u'Submitted Assignment')
		verbose_name_plural = _(u'Submitted Assignments')
		ordering = ('-date_created',)

	def __str__(self):
		return "%s: %s" % (self.student, self.assignment.question[:20])