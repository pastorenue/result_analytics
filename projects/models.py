from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class Project(models.Model):
    '''Personal and school projects that a student can participate in'''

    student = models.ForeignKey('students.Student', related_name='projects', null=True)
    name = models.CharField(max_length=250, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, null=True)
    file = models.FileField(upload_to='students/projects/%Y/%m/%d/', blank=True)
    date_created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    tag = models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = _(u'Student Project')
        verbose_name_plural = _(u'Student Projects')
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
    	orig = slugify(self.name)
    	self.slug = "%s-%s" % (orig, uuid.uuid4())
    	super(Project, self).save(**kwargs)

    #@models.permalink
    def get_absolute_url(self):
    	return reverse('project_detail', args=[self.pk, self.slug])


class ProjectSupervision(models.Model):
	ACTIVE, DECLINED, COMPLETED, REVOKED = ('A', 'D', 'C', 'R')
	PROJECT_STATUS = (
		(ACTIVE, 'Active'),
		(DECLINED, 'Declined'),
		(COMPLETED, 'Completed'),
		(REVOKED, 'Revoked')
	)
	lecturer = models.ForeignKey('institutions.Lecturer', null=True)
	project = models.ForeignKey(Project, null=True)
	status = models.CharField(max_length=1, choices=PROJECT_STATUS, default='A')
	last_checked = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return "%s-->%s" % (lecturer, self.project)


