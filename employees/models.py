from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from salary.models import PayTemplate
from organization.models import Position, Location, Unit, GradeLevel
from states.models import Country, LGA, State
from django.db.models import signals
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from changerequest.models import ChangeTrackingModel
from configstore.configs import ConfigurationInstance, register
from configstore.forms import ConfigurationForm
from dynamicgroups.lookups import LookupBase, Field as Lookup
from dynamicgroups.models import Group
import uuid

# Marital status constants:
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

RELIGION_CHOICES = (
    (1, 'Christianity'),
    (2, 'Islam'),
    (300, 'Others'),
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

# Relationship constants:
(FATHER, MOTHER, HUSBAND, WIFE, AUNT, UNCLE, CHILD,
 BROTHER, SISTER, COUSIN, NEPHEW, NIECE, OTHERS) = range(1, 14)
RELATIONSHIP_CHOICES = (
    (FATHER, _(u'Father')),
    (MOTHER, _(u'Mother')),
    (HUSBAND, _(u'Husband')),
    (WIFE, _(u'Wife')),
    (AUNT, _(u'Aunt')),
    (UNCLE, _(u'Uncle')),
    (CHILD, _(u'Child')),
    (BROTHER, _(u'Brother')),
    (SISTER, _(u'Sister')),
    (COUSIN, _(u'Cousin')),
    (NEPHEW, _(u'Nephew')),
    (NIECE, _(u'Niece')),
    (OTHERS, _(u'Others'))
)

EMPLOYEE_TITLES = (
    (1, 'Mr'),
    (2, 'Mrs'),
    (3, 'Miss'),
    (4, 'Dr'),
    (5, 'Prof'),
    (6, 'Mallam'),
    (7, 'Chief'),
    (8, 'Alhaji'),
    (9, 'Alhaja'),
    (10, 'J.P.'),
)

######################
## Employee Options ##
######################

class EmployeeOptionsForm(ConfigurationForm):
    probation_period = forms.IntegerField(min_value=1, label=_(u'Probation Period'), initial=4,
                                          help_text=_(u'Default probation period (in weeks) for new employees.'))
    hr_group = forms.ModelChoiceField(queryset=Group.objects.all(), label=_(u'HR Group'),
                                      help_text=_(u'This is the group responsible for HR tasks.'))

employee_options = ConfigurationInstance('employee_options', _(u'Employee Options'), EmployeeOptionsForm)
register(employee_options)

##############
## Managers ##
##############

class BankManager(models.Manager):
    """'Twas only a matter of time before we got one of these :)"""

    def get_by_natural_key(self, name):
        return self.get(name=name)

class EmployeeManager(models.Manager):
    def get_active_employees(self):
        """Returns all employees, still in employment (excluding ex-employees)."""
        #return super(EmployeeManager, self).get_query_set().exclude(status=Employee.EX_EMPLOYEE)

class PlacementManager(models.Manager):
    def from_employee(self, employee, start_date=None):
        """Creates a new Placement from the employee's current position and location."""
        return super(PlacementManager, self).create(
            employee=employee,
            position=employee.position,
            unit=employee.unit,
            location=employee.location,
            start_date=(start_date or employee.hire_date))

############
## Models ##
############

class EmployeeType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = _(u'Employee Type')
        verbose_name_plural = _(u'Employee Types')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=150, unique=True)

    objects = BankManager()

    class Meta:
        verbose_name = _(u'Bank')
        verbose_name_plural = _(u'Banks')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

class PensionCustodian(models.Model):
    name = models.CharField(max_length=150, unique=True)
    bank = models.ForeignKey(Bank, null=True, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    sort_code = models.CharField(max_length=20, blank=True)
    contact = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        verbose_name = _(u'Pension Custodian')
        verbose_name_plural = _(u'Pension Custodians')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class PensionAdministrator(models.Model):
    name = models.CharField(max_length=150, unique=True)
    custodian = models.ForeignKey(PensionCustodian, null=True, blank=True)
    account_name = models.CharField(max_length=50, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    sort_code = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        verbose_name = _(u'Pension Administrator')
        verbose_name_plural = _(u'Pension Administrators')
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Employee(ChangeTrackingModel):
    (ONLEAVE, RESIGNED, RETIRED, DISMISSED,
    ACTIVE, SUSPENDED, EX_EMPLOYEE) = range(7)
    STATUS_CHOICES = (
        (ONLEAVE, _(u'On Leave')),
        (RESIGNED, _(u'Resigned')),
        (RETIRED, _(u'Retired')),
        (DISMISSED, _(u'Dismissed')),
        (ACTIVE, _(u'Active')),
        (SUSPENDED, _(u'On Suspension')),
        (EX_EMPLOYEE, _(u'Ex Employee')),
    )

    user = models.OneToOneField(User, related_name='employee')
    staff_id_number = models.CharField(verbose_name=_(u'Staff ID'), max_length=30, unique=True, blank=True, db_index=True,
        help_text=_(u"Leave this blank to auto-generate a Staff ID"))
    photo = models.ImageField(upload_to='employees/photos/%Y/%m/', blank=True)
    title = models.PositiveIntegerField(choices=EMPLOYEE_TITLES, blank=True, null=True)
    first_name = models.CharField(verbose_name=_(u'First name'), max_length=50, blank=True)
    middle_name = models.CharField(verbose_name=_(u'Middle name'), max_length=50, blank=True)
    last_name = models.CharField(verbose_name=_(u'Surname'), max_length=50, blank=True)
    marital_status = models.PositiveSmallIntegerField(choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='F')
    birth_date = models.DateField(blank=True, null=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    address = models.TextField(blank=True)
    grade_level = models.ForeignKey(GradeLevel, related_name='employees')
    basic = models.DecimalField(verbose_name=_(u'Gross pay'), max_digits=14, decimal_places=2, blank=True, null=True,
        help_text=_(u"Leave this blank to use the value defined by this employee's Grade Level"))
    pay_template = models.ForeignKey(PayTemplate, related_name='employees')
    position = models.ForeignKey(Position, related_name='employees', help_text=_(u"This employee's job title"))
    unit = models.ForeignKey(Unit, related_name='employees', help_text=_(u"The department or division this employee is being assigned to"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    hire_date = models.DateField()
    confirmation_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    location = models.ForeignKey(Location, related_name='employees')
    employee_type = models.ForeignKey(EmployeeType, blank=True, null=True)
    bank = models.ForeignKey(Bank, blank=True, null=True)
    bank_account_number = models.CharField(max_length=20, blank=True, null=True)
    skip_pension = models.BooleanField(default=False, verbose_name=_(u"Skip pension"))
    skip_nhf = models.BooleanField(default=False, verbose_name=_(u"Skip NHF"))
    skip_nhis = models.BooleanField(default=False, verbose_name=_(u"Skip NHIS"))
    skip_nsitf = models.BooleanField(default=False, verbose_name=_(u"Skip NSITF"))
    pension_administrator = models.ForeignKey(PensionAdministrator, blank=True, null=True)
    pfa_pin = models.CharField(max_length=50, verbose_name=_(u'PFA PIN'), blank=True, null=True)
    tax_id = models.CharField(max_length=20, blank=True)
    maiden_name = models.CharField(max_length=50, blank=True)
    mothers_maiden_name = models.CharField(verbose_name=_(u"Mother's maiden name"), max_length=50, blank=True)
    religion = models.PositiveSmallIntegerField(choices=RELIGION_CHOICES, blank=True, null=True)
    blood_group = models.CharField(max_length=2, choices=BLOOD_GROUP_CHOICES, blank=True)
    genotype = models.CharField(max_length=2, choices=GENOTYPE_CHOICES, blank=True)
    national_id_number = models.CharField(verbose_name=_(u"National ID Number"), max_length=50, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    permanent_address = models.TextField(blank=True)
    state_of_residence = models.ForeignKey(State, related_name='employees_residence',
        help_text=_(u'Your income tax will be remitted to this state.'))
    country = models.ForeignKey(Country, related_name='country_of_residence', null=True, blank=True)
    state_of_origin = models.ForeignKey(State, related_name='employees_origin', blank=True, null=True)
    lga = models.ForeignKey(LGA, verbose_name=_(u'LGA'), related_name='employees', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = EmployeeManager()

    class Meta:
        verbose_name = _(u'Employee')
        verbose_name_plural = _(u'Employees')
        ordering = ('user__first_name', 'user__last_name',)
        unique_together = (
            ('bank', 'bank_account_number'),
            ('pension_administrator', 'pfa_pin'),
        )
        permissions = (
            ('can_manage_employees', u'Can manage employees'),
            ('can_export_employees', u'Can export employee data'),
        )

    def __unicode__(self):
        return self.full_name

    @models.permalink
    def get_absolute_url(self):
        return ('employees_employee_profile', (), {'employee_id': self.pk})

    @property
    def full_name(self):
        """Returns this employee's full name."""
        names = [self.first_name]
        if self.middle_name:
            names.append(self.middle_name)
        names.append(self.last_name)
        return u' '.join(names)

    @property
    def employee_basic(self):
        """Returns `self.basic`, defaulting to `self.grade_level basic`."""
        return self.basic or self.grade_level.basic

    @property
    def num_children(self):
        return self.dependents.filter(relationship=CHILD).count()

    @property
    def num_dependents(self):
        return self.dependents.count()

    @property
    def has_disability(self):
        return False

    @property
    def include_pension(self):
        # Do we really need this and `skip_pension`?
        # They seem like opposites of each other, which could be confusing.
        # Unless, of course, this property does something entirely different (oops)...
        return not self.skip_pension

    @property
    def is_leaving(self):
        # If this is a boolean property, `.exists` will be a bit more efficient (and easier to read).
        # Otherwise, Stan is an idiot and should learn to leave well enough alone...
        return self.terminations.exists()


class NextOfKin(ChangeTrackingModel):
    """Record of an employee's next of kin."""

    employee = models.ForeignKey(Employee, related_name='next_of_kin', editable=False)
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    relationship = models.PositiveSmallIntegerField(choices=RELATIONSHIP_CHOICES)

    class Meta:
        verbose_name = _(u'Next Of Kin')
        verbose_name_plural = _(u'Next Of Kin')
        ordering = ('name',)

    def __unicode__(self):
        return u'%s (%s of %s)' % (
            self.name,
            self.get_relationship_display(),
            self.employee
        )

class Dependent(ChangeTrackingModel):
    """Record of an employee's dependents, used for tax relief."""

    employee = models.ForeignKey(Employee, related_name='dependents', editable=False)
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    birth_date = models.DateField()
    relationship = models.PositiveSmallIntegerField(choices=RELATIONSHIP_CHOICES)

    class Meta:
        verbose_name = _(u'Dependent')
        verbose_name_plural = _(u'Dependents')
        ordering = ('name',)

    def __unicode__(self):
        return u'%s (%s of %s)' % (
            self.name,
            self.get_relationship_display(),
            self.employee
        )
    

class Education(ChangeTrackingModel):
    """Record of an employee's qualifications."""

    employee = models.ForeignKey('Employee', related_name='institutions', editable=False)
    name = models.CharField(verbose_name=_(u'Institution'), max_length=100)
    start_date = models.DateField(verbose_name=_(u'From'))
    end_date = models.DateField(verbose_name=_(u'To'))
    course_studied = models.CharField(max_length=100)
    grade_obtained = models.CharField(max_length=30, blank=True)
    degree = models.CharField(verbose_name=_(u'Degree or Certification obtained'), max_length=30)
    remarks = models.TextField(blank=True)

    class Meta:
        verbose_name = _(u'Education')
        verbose_name_plural = _(u'Education')
        ordering = ('-start_date', '-end_date',)

    def __unicode__(self):
        return u'%s: %s from %s (%s to %s)' % (
            self.employee,
            self.degree,
            self.name,
            self.start_date.strftime('%d %b %Y'),
            self.end_date.strftime('%d %b %Y')
        )

class Experience(ChangeTrackingModel):
    """Record of an employee's previous work experience."""

    employee = models.ForeignKey('Employee', related_name='experience', editable=False)
    organization = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    remarks = models.TextField(blank=True)

    class Meta:
        verbose_name = _(u'Work Experience')
        verbose_name_plural = _(u'Work Experience')
        ordering = ('-start_date', '-end_date',)

    def __unicode__(self):
        return u'%s: %s at %s (from %s to %s)' % (
            self.employee,
            self.position,
            self.organization,
            self.start_date.strftime('%d %b %Y'),
            self.end_date.strftime('%d %b %Y')
        )

class Placement(models.Model):
    """A snapshot of an employee's position within a company."""

    employee = models.ForeignKey('Employee', related_name='placements')
    position = models.ForeignKey('organization.Position', related_name='placements')
    unit = models.ForeignKey('organization.Unit', related_name='placements')
    location = models.ForeignKey('organization.Location', related_name='placements')
    start_date = models.DateField()
    role = models.TextField(blank=True)

    objects = PlacementManager()

    class Meta:
        verbose_name = _(u'Placement')
        verbose_name_plural = _(u'Placements')
        ordering = ('-id',)

    def __unicode__(self):
        return u'%s: %s/%s' % (self.employee.full_name, self.position, self.unit)

class Termination(models.Model):
    """Records an employee leaving a company."""

    employee = models.ForeignKey('Employee', related_name='terminations')
    reason = models.CharField(max_length=100, blank=True)
    exit_date = models.DateField(help_text=_(u"After this date, this employee's status will be 'Ex-Employee'."))
    last_process_date = models.DateField(help_text=_(u"This employee's payroll will not be processed after this date."))
    user = models.ForeignKey(User, related_name='terminations') # FIXME: Is this really necessary?

    class Meta:
        verbose_name = _(u'Termination')
        verbose_name_plural = _(u'Terminations')

    def __unicode__(self):
        return self.employee.full_name

def slug_default():
    return uuid.uuid4().hex

class Document(ChangeTrackingModel):
    """Represents electronic documents that form part of an employee's record."""

    uid = models.SlugField(max_length=32, default=slug_default(), editable=False)
    employee = models.ForeignKey('Employee', related_name='documents', editable=False)
    ctype = models.ForeignKey(ContentType, null=True, editable=False)
    object_id = models.PositiveIntegerField(null=True, editable=False)
    attached_to = generic.GenericForeignKey('ctype', 'object_id')
    file = models.FileField(upload_to='employees/docs/%Y/%m/%d/')
    name = models.CharField(max_length=255, editable=False)
    description = models.TextField(_(u'Description'), blank=True)
    created_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name = _(u'Document')
        verbose_name_plural = _(u'Documents')

    def __unicode__(self):
        return self.name

    def delete(self, **kwargs):
        self.file.delete()
        return super(Document, self).delete(**kwargs)

class InsuranceCompany(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = _(u'Insurance Company')
        verbose_name_plural = _(u'Insurance Companies')

    def __unicode__(self):
        return self.name

class LifeInsurance(ChangeTrackingModel):
    employee = models.ForeignKey('Employee', related_name='insurance_policies')
    insurer = models.ForeignKey('InsuranceCompany', related_name='policies')
    policy_number = models.CharField(max_length=50)
    monthly_rate =models.DecimalField(_(u'Monthly premium'), decimal_places=2, max_digits=10)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _(u'Life Insurance Policy')
        verbose_name_plural = _(u'Life Insurance Policies')

    def __unicode__(self):
        return unicode(self.employee)

class IncidenceType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    class Meta:
        verbose_name = _(u'Incidence Type')
        verbose_name_plural = _(u'Incidence Types')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Incidence(models.Model):
    employee = models.ForeignKey(Employee, related_name='employee_incidences')
    incidence_type = models.ForeignKey(IncidenceType)
    title = models.CharField(max_length=50)
    record_date = models.DateField(auto_now_add=True)
    incidence_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)

###############################
## Dynamic Group Definitions ##
###############################

class EmployeeLookupCriteria(LookupBase):
    """Register the Employee model with the dynamic query framework."""

    model = Employee
    fields = (
        Lookup('staff_id_number'),
        Lookup('grade_level', 'name'),
        Lookup('position', 'name'),
        #Lookup('position__reports__employees__user', description=_(u'Supervisor for user')),
        Lookup('unit', 'name'),
        #Lookup('unit__employees__user', description=_(u'Same unit as user')),
        Lookup('location', 'name'),
        #Lookup('location__employees__user', description=_(u'Same location as user')),
        Lookup('employee_type', 'name'),
        Lookup('bank', 'name'),
        Lookup('pension_administrator', 'name'),
        Lookup('state_of_residence', 'name'),
        Lookup('hire_date'),
        Lookup('confirmation_date'),
        Lookup('termination_date'),
    )

#####################
## Signal Handlers ##
#####################

def record_initial_placement(sender, **kwds):
    """Records an employee's initial placement, when the employee is added."""
    if kwds['created']:
        Placement.objects.from_employee(kwds['instance'])

signals.post_save.connect(record_initial_placement, sender=Employee, dispatch_uid=record_initial_placement.__name__)

# Enable Custom Fields for the Employee model:
from extendmodels import register
register(Employee)
