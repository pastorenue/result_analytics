# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Banks',
            },
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True)),
                ('birth_date', models.DateField()),
                ('relationship', models.PositiveSmallIntegerField(choices=[(1, 'Father'), (2, 'Mother'), (3, 'Husband'), (4, 'Wife'), (5, 'Aunt'), (6, 'Uncle'), (7, 'Child'), (8, 'Brother'), (9, 'Sister'), (10, 'Cousin'), (11, 'Nephew'), (12, 'Niece'), (13, 'Others')])),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Dependent',
                'verbose_name_plural': 'Dependents',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.SlugField(default=b'dbdcc04a6ce94a6d806bfabeb940790e', max_length=32, editable=False)),
                ('object_id', models.PositiveIntegerField(null=True, editable=False)),
                ('file', models.FileField(upload_to=b'employees/docs/%Y/%m/%d/')),
                ('name', models.CharField(max_length=255, editable=False)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Institution')),
                ('start_date', models.DateField(verbose_name='From')),
                ('end_date', models.DateField(verbose_name='To')),
                ('course_studied', models.CharField(max_length=100)),
                ('grade_obtained', models.CharField(max_length=30, blank=True)),
                ('degree', models.CharField(max_length=30, verbose_name='Degree or Certification obtained')),
                ('remarks', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('-start_date', '-end_date'),
                'verbose_name': 'Education',
                'verbose_name_plural': 'Education',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('staff_id_number', models.CharField(max_length=30, blank=True, help_text='Leave this blank to auto-generate a Staff ID', unique=True, verbose_name='Staff ID', db_index=True)),
                ('photo', models.ImageField(upload_to=b'employees/photos/%Y/%m/', blank=True)),
                ('title', models.PositiveIntegerField(blank=True, null=True, choices=[(1, b'Mr'), (2, b'Mrs'), (3, b'Miss'), (4, b'Dr'), (5, b'Prof'), (6, b'Mallam'), (7, b'Chief'), (8, b'Alhaji'), (9, b'Alhaja'), (10, b'J.P.')])),
                ('first_name', models.CharField(max_length=50, verbose_name='First name', blank=True)),
                ('middle_name', models.CharField(max_length=50, verbose_name='Middle name', blank=True)),
                ('last_name', models.CharField(max_length=50, verbose_name='Surname', blank=True)),
                ('marital_status', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, 'Single'), (2, 'Married'), (3, 'Widowed'), (4, 'Divorced')])),
                ('sex', models.CharField(default=b'F', max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('birth_date', models.DateField(db_index=True, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('address', models.TextField(blank=True)),
                ('basic', models.DecimalField(decimal_places=2, max_digits=14, blank=True, help_text="Leave this blank to use the value defined by this employee's Grade Level", null=True, verbose_name='Gross pay')),
                ('status', models.PositiveSmallIntegerField(default=4, choices=[(0, 'On Leave'), (1, 'Resigned'), (2, 'Retired'), (3, 'Dismissed'), (4, 'Active'), (5, 'On Suspension'), (6, 'Ex Employee')])),
                ('hire_date', models.DateField()),
                ('confirmation_date', models.DateField(null=True, blank=True)),
                ('termination_date', models.DateField(null=True, blank=True)),
                ('bank_account_number', models.CharField(max_length=20, null=True, blank=True)),
                ('skip_pension', models.BooleanField(default=False, verbose_name='Skip pension')),
                ('skip_nhf', models.BooleanField(default=False, verbose_name='Skip NHF')),
                ('skip_nhis', models.BooleanField(default=False, verbose_name='Skip NHIS')),
                ('skip_nsitf', models.BooleanField(default=False, verbose_name='Skip NSITF')),
                ('pfa_pin', models.CharField(max_length=50, null=True, verbose_name='PFA PIN', blank=True)),
                ('tax_id', models.CharField(max_length=20, blank=True)),
                ('maiden_name', models.CharField(max_length=50, blank=True)),
                ('mothers_maiden_name', models.CharField(max_length=50, verbose_name="Mother's maiden name", blank=True)),
                ('religion', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, b'Christianity'), (2, b'Islam'), (300, b'Others')])),
                ('blood_group', models.CharField(blank=True, max_length=2, choices=[(b'A', b'A'), (b'AB', b'AB'), (b'B', b'B'), (b'O+', b'O+'), (b'O-', b'O-')])),
                ('genotype', models.CharField(blank=True, max_length=2, choices=[(b'AA', b'AA'), (b'AS', b'AS'), (b'SS', b'SS')])),
                ('national_id_number', models.CharField(max_length=50, verbose_name='National ID Number', blank=True)),
                ('passport_number', models.CharField(max_length=20, blank=True)),
                ('permanent_address', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('user__first_name', 'user__last_name'),
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'permissions': (('can_manage_employees', 'Can manage employees'), ('can_export_employees', 'Can export employee data')),
            },
        ),
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Employee Type',
                'verbose_name_plural': 'Employee Types',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('remarks', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('-start_date', '-end_date'),
                'verbose_name': 'Work Experience',
                'verbose_name_plural': 'Work Experience',
            },
        ),
        migrations.CreateModel(
            name='Incidence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('record_date', models.DateField(auto_now_add=True)),
                ('incidence_date', models.DateField()),
                ('remarks', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncidenceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Incidence Type',
                'verbose_name_plural': 'Incidence Types',
            },
        ),
        migrations.CreateModel(
            name='InsuranceCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Insurance Company',
                'verbose_name_plural': 'Insurance Companies',
            },
        ),
        migrations.CreateModel(
            name='LifeInsurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('policy_number', models.CharField(max_length=50)),
                ('monthly_rate', models.DecimalField(verbose_name='Monthly premium', max_digits=10, decimal_places=2)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Life Insurance Policy',
                'verbose_name_plural': 'Life Insurance Policies',
            },
        ),
        migrations.CreateModel(
            name='NextOfKin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('address', models.TextField(blank=True)),
                ('phone', models.CharField(max_length=30, blank=True)),
                ('relationship', models.PositiveSmallIntegerField(choices=[(1, 'Father'), (2, 'Mother'), (3, 'Husband'), (4, 'Wife'), (5, 'Aunt'), (6, 'Uncle'), (7, 'Child'), (8, 'Brother'), (9, 'Sister'), (10, 'Cousin'), (11, 'Nephew'), (12, 'Niece'), (13, 'Others')])),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Next Of Kin',
                'verbose_name_plural': 'Next Of Kin',
            },
        ),
        migrations.CreateModel(
            name='PensionAdministrator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('account_name', models.CharField(max_length=50, blank=True)),
                ('account_number', models.CharField(max_length=50, blank=True)),
                ('sort_code', models.CharField(max_length=50, blank=True)),
                ('contact', models.CharField(max_length=50, blank=True)),
                ('address', models.TextField(blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('website', models.URLField(blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Pension Administrator',
                'verbose_name_plural': 'Pension Administrators',
            },
        ),
        migrations.CreateModel(
            name='PensionCustodian',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('account_number', models.CharField(max_length=20, blank=True)),
                ('sort_code', models.CharField(max_length=20, blank=True)),
                ('contact', models.CharField(max_length=50, blank=True)),
                ('address', models.TextField(blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('website', models.URLField(blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Pension Custodian',
                'verbose_name_plural': 'Pension Custodians',
            },
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('role', models.TextField(blank=True)),
                ('employee', models.ForeignKey(related_name='placements', to='employees.Employee')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'Placement',
                'verbose_name_plural': 'Placements',
            },
        ),
        migrations.CreateModel(
            name='Termination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=100, blank=True)),
                ('exit_date', models.DateField(help_text="After this date, this employee's status will be 'Ex-Employee'.")),
                ('last_process_date', models.DateField(help_text="This employee's payroll will not be processed after this date.")),
                ('employee', models.ForeignKey(related_name='terminations', to='employees.Employee')),
                ('user', models.ForeignKey(related_name='terminations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Termination',
                'verbose_name_plural': 'Terminations',
            },
        ),
    ]
