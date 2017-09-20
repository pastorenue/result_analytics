from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from institutions.models import *
import uuid
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import signals
from django.utils.timezone import now
from river.models.fields.state import StateField


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

(REGULAR, SANDWICH, CEP, DIPLOMA, OTHERS) = range(1,6)
PROGRAM_CHOICES = (
    (REGULAR, _(u'Regular')),
    (SANDWICH, (u'Sandwich')),
    (CEP, (u'CEP')),
    (DIPLOMA, (u'Diploma')),
    (OTHERS, (u'Others')),
)

RELIGION_CHOICES = (
    (1, 'Christianity'),
    (2, 'Islam'),
    (3, 'Others'),
)

BLOOD_GROUP_CHOICES = (
    ('A', 'A'),
    ('AB', 'AB'),
    ('B', 'B'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)

GENOTYPE_CHOICES = (
    ('AA', 'AA'),
    ('AS', 'AS'),
    ('SS', 'SS'),
)


class StudentManager(models.Manager):
    def get_active_students(self):
        """Returns all employees, still in employment (excluding ex-employees)."""
        return super(StudentManager, self).get_query_set().exclude(status='E')


class Bank(models.Model):
    name = models.CharField(max_length=150, unique=True)


    class Meta:
        verbose_name = _(u'Bank')
        verbose_name_plural = _(u'Banks')
        ordering = ('name',)

    def __str__(self):
        return self.name


class PhoneCategory(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = _(u'Phone Category')
        verbose_name_plural = _(u'Phone Categories')
        ordering = ('name',)

    def __str__(self):
        return self.name




class Student(models.Model):
    STATUS_CHOICES = (
        ('A', _(u'Active')),
        ('G', _(u'Graduated')),
        ('S', _(u'Suspended')),
        ('E', _(u'Expelled')),
    )

    user = models.OneToOneField(User, related_name='student', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads', blank=True)
    email = models.EmailField(blank=True)
    last_name = models.CharField(verbose_name=_(u'Surname'), max_length=50, null=True)
    first_name = models.CharField(verbose_name=_(u'First name'), max_length=50, null=True)
    middle_name = models.CharField(verbose_name=_(u'Middle name'), max_length=50, blank=True)
    user_status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='A', blank=True, null=True)
    reg_number = models.CharField(max_length=30)
    faculty= models.ForeignKey(Faculty, null=True)
    department = models.ForeignKey(Department, null=True)
    bank = models.ForeignKey(Bank, blank=True, null=True)
    bank_account_number = models.CharField(max_length=20, blank=True, null=True)
    marital_status = models.PositiveSmallIntegerField(choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    sex = models.CharField(max_length=1, null=True, choices=SEX_CHOICES)
    level = models.PositiveIntegerField(choices=settings.LEVEL_CHOICES, blank=True)
    institution = models.ForeignKey(Institution, null=True)
    program_type = models.PositiveIntegerField(choices=PROGRAM_CHOICES, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True, db_index=True)
    library_id_number = models.PositiveIntegerField(blank=True, null=True)
    school_id_number = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_gained_admission = models.DateField(auto_now=True)
    blood_group = models.CharField(max_length=2, choices=BLOOD_GROUP_CHOICES, blank=True)
    genotype = models.CharField(max_length=2, choices=GENOTYPE_CHOICES, blank=True)
    national_id_number = models.CharField(verbose_name=_(u"National ID Number"), max_length=50, blank=True)
    year_of_admission = models.DateField()
    course_duration = models.PositiveIntegerField()
    religion = models.PositiveIntegerField(choices=RELIGION_CHOICES, blank=True, null=True)
    permanent_address = models.TextField(blank=True)
    state_of_residence = models.ForeignKey('states.State', null=True,blank=True, related_name='students_residence')
    country = models.ForeignKey('states.Country', related_name='country_of_residence', null=True, blank=True)
    state_of_origin = models.ForeignKey('states.State', related_name='students_origin', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    #clearance_status = StateField(editable=False, default=None)
    slug = models.SlugField(blank=True, unique=True)
    objects = StudentManager()


    class Meta:
        verbose_name = _(u'Student')
        verbose_name_plural = _(u'Students')
        ordering = ('last_name',)
        
        

    def __str__(self):
        names = [self.last_name]
        if self.middle_name:
            names.append(self.middle_name)
        names.append(self.first_name)
        return u' '.join(names)


    @property
    def full_name(self):
        """Returns this employee's full name."""
        names = [self.last_name]
        if self.middle_name:
            names.append(self.middle_name)
        names.append(self.first_name)
        return u' '.join(names)
    
    @property
    def is_student(self):
        return True

    @property
    def get_program_type(self):
        program_type = {1: 'Regular', 2: 'Sandwich', 3: 'CEP', 4: 'Diploma', 5: 'Others'}
        if self.program_type:
            return program_type[self.program_type]

    @property
    def get_marital_status(self):
        marital_status = {1: 'Single', 2: 'Married', 3: 'Widowed', 4: 'Divorces'}
        if self.marital_status:
            return marital_status[self.marital_status]
        
    @property
    def year_of_graduation(self):
        if self.year_of_admission:
            return (self.year_of_admission.year + self.course_duration)
    
    def get_absolute_url(self):
        return reverse('students:student_account', kwargs={'student_slug':self.slug})


class Document(models.Model):
    """Represents electronic documents that form part of a student's record."""

    student = models.ForeignKey(Student)
    attached_file = models.FileField(upload_to='uploads/docs/%Y/%m/%d/')
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(_(u'Description'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _(u'Attached Document')
        verbose_name_plural = _(u'Attached Documents')

    def __str__(self):
        return self.name

    def delete(self, **kwargs):
        self.file.delete()
        return super(Document, self).delete(**kwargs)
    
    def current_level(self):
        level = (self.level+100)
        return level

class Scholarship(models.Model):
    '''Scholarship schemes a student is involved in or wishes to be involved in'''
    student = models.ForeignKey(Student, null=True, blank=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    provider = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Scholarship')
        verbose_name_plural = _(u'Scholarships')
        ordering = ('title',)

    def __str__(self):
        return "%s" %(self.title)


class UniqueMapper(models.Model):
    reg_number = models.CharField(max_length=30)
    short_institution_name = models.CharField(max_length=5, null=True)
    unique_map = models.CharField(max_length=50, blank=True)
    created = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name = _(u'Unique Mapper')
        verbose_name_plural = _(u'Unique Mappers')
        ordering = ('short_institution_name',)

    def __str__(self):
        return "%s-%s" % (self.short_institution_name.upper(), self.unique_map)


    def save(self, **kwargs):
        uuid_found = True
        while uuid_found:
            get_uuid = uuid.uuid4()
            self.unique_map = "%s-%s" % (self.short_institution_name, get_uuid)
            if not UniqueMapper.objects.filter(unique_map=self.unique_map).exists():
                uuid_found = False
        super(UniqueMapper, self).save(**kwargs)


