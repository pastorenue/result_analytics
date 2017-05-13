# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('states', '0001_initial'),
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Banks',
                'verbose_name': 'Bank',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(editable=False, null=True)),
                ('file', models.FileField(upload_to='students/docs/%Y/%m/%d/')),
                ('name', models.CharField(editable=False, max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ctype', models.ForeignKey(null=True, editable=False, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Attached Documents',
                'verbose_name': 'Attached Document',
            },
        ),
        migrations.CreateModel(
            name='PhoneCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Phone Categories',
                'verbose_name': 'Phone Category',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('number', models.CharField(max_length=15, null=True)),
                ('category', models.ForeignKey(null=True, to='students.PhoneCategory')),
            ],
            options={
                'ordering': ('category',),
                'verbose_name_plural': 'Phone Numbers',
                'verbose_name': 'Phone Number',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='students/projects/%Y/%m/%d/')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
                ('tag', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Student Projects',
                'verbose_name': 'Student Project',
            },
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('provider', models.CharField(blank=True, max_length=250, null=True)),
                ('location', models.CharField(blank=True, max_length=150, null=True)),
                ('website', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Scholarships',
                'verbose_name': 'Scholarship',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='students/photos/%Y/%m/')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='First name')),
                ('middle_name', models.CharField(blank=True, max_length=50, verbose_name='Middle name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Surname')),
                ('user_status', models.CharField(null=True, blank=True, max_length=50, choices=[(1, 'Barred'), (0, 'Active'), (2, 'Inactive')])),
                ('reg_number', models.CharField(max_length=30)),
                ('bank_account_number', models.CharField(blank=True, max_length=20, null=True)),
                ('marital_status', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, 'Single'), (2, 'Married'), (3, 'Widowed'), (4, 'Divorced')])),
                ('sex', models.CharField(default='M', max_length=1, choices=[('M', 'Male'), ('F', 'Female')])),
                ('level', models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('program_type', models.PositiveIntegerField(null=True, choices=[(1, 'Regular'), (2, 'Sandwich'), (3, 'CEP'), (4, 'Diploma'), (5, 'Others')])),
                ('birth_date', models.DateField(blank=True, db_index=True, null=True)),
                ('library_id_number', models.PositiveIntegerField(blank=True, null=True)),
                ('school_id_number', models.PositiveIntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.TextField(blank=True)),
                ('date_gained_admission', models.DateField(auto_now=True)),
                ('blood_group', models.CharField(blank=True, max_length=2, choices=[('A', 'A'), ('AB', 'AB'), ('B', 'B'), ('O+', 'O+'), ('O-', 'O-')])),
                ('genotype', models.CharField(blank=True, max_length=2, choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS')])),
                ('national_id_number', models.CharField(blank=True, max_length=50, verbose_name='National ID Number')),
                ('year_of_graduation', models.PositiveIntegerField()),
                ('religion', models.PositiveIntegerField(blank=True, null=True, choices=[(1, 'Christianity'), (2, 'Islam'), (300, 'Others')])),
                ('permanent_address', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('bank', models.ForeignKey(null=True, blank=True, to='students.Bank')),
                ('country', models.ForeignKey(null=True, blank=True, related_name='country_of_residence', to='states.Country')),
                ('department', models.ForeignKey(null=True, to='institutions.Department')),
                ('faculty', models.ForeignKey(null=True, to='institutions.Faculty')),
                ('lga', models.ForeignKey(verbose_name='LGA', null=True, blank=True, related_name='students', to='states.LGA')),
                ('state_of_origin', models.ForeignKey(null=True, blank=True, related_name='students_origin', to='states.State')),
                ('state_of_residence', models.ForeignKey(null=True, blank=True, related_name='students_residence', to='states.State')),
                ('student_institution', models.ForeignKey(null=True, blank=True, to='institutions.Institution')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='student')),
            ],
            options={
                'ordering': ('user__first_name', 'user__last_name'),
                'verbose_name_plural': 'Students',
                'verbose_name': 'Student',
            },
        ),
        migrations.AddField(
            model_name='scholarship',
            name='student',
            field=models.ForeignKey(null=True, blank=True, related_name='scholarship', to='students.Student'),
        ),
        migrations.AddField(
            model_name='project',
            name='student',
            field=models.ForeignKey(null=True, blank=True, related_name='projects', to='students.Student'),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='students',
            field=models.ForeignKey(to='students.Student', null=True, related_name='phone'),
        ),
        migrations.AddField(
            model_name='document',
            name='students',
            field=models.ForeignKey(editable=False, related_name='documents', to='students.Student'),
        ),
    ]
