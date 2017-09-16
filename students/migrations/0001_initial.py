# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('states', '0001_initial'),
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Banks',
                'verbose_name': 'Bank',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('attached_file', models.FileField(upload_to='uploads/docs/%Y/%m/%d/')),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Attached Documents',
                'verbose_name': 'Attached Document',
            },
        ),
        migrations.CreateModel(
            name='PhoneCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=30, blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Phone Categories',
                'verbose_name': 'Phone Category',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=250, blank=True, null=True)),
                ('provider', models.CharField(max_length=250, blank=True, null=True)),
                ('location', models.CharField(max_length=150, blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Scholarships',
                'verbose_name': 'Scholarship',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('photo', models.ImageField(blank=True, upload_to='uploads')),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('last_name', models.CharField(verbose_name='Surname', max_length=50, null=True)),
                ('first_name', models.CharField(verbose_name='First name', max_length=50, null=True)),
                ('middle_name', models.CharField(max_length=50, verbose_name='Middle name', blank=True)),
                ('user_status', models.CharField(default='A', choices=[('A', 'Active'), ('G', 'Graduated'), ('S', 'Suspended'), ('E', 'Expelled')], blank=True, max_length=1, null=True)),
                ('reg_number', models.CharField(max_length=30)),
                ('bank_account_number', models.CharField(max_length=20, blank=True, null=True)),
                ('marital_status', models.PositiveSmallIntegerField(choices=[(1, 'Single'), (2, 'Married'), (3, 'Widowed'), (4, 'Divorced')], blank=True, null=True)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('level', models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('program_type', models.PositiveIntegerField(choices=[(1, 'Regular'), (2, 'Sandwich'), (3, 'CEP'), (4, 'Diploma'), (5, 'Others')], null=True)),
                ('birth_date', models.DateField(db_index=True, blank=True, null=True)),
                ('library_id_number', models.PositiveIntegerField(blank=True, null=True)),
                ('school_id_number', models.PositiveIntegerField(blank=True, null=True)),
                ('address', models.CharField(max_length=100, blank=True, null=True)),
                ('phone_number', models.CharField(max_length=15, blank=True, null=True)),
                ('date_gained_admission', models.DateField(auto_now=True)),
                ('blood_group', models.CharField(max_length=2, choices=[('A', 'A'), ('AB', 'AB'), ('B', 'B'), ('O+', 'O+'), ('O-', 'O-')], blank=True)),
                ('genotype', models.CharField(max_length=2, choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS')], blank=True)),
                ('national_id_number', models.CharField(max_length=50, verbose_name='National ID Number', blank=True)),
                ('year_of_admission', models.DateField()),
                ('course_duration', models.PositiveIntegerField()),
                ('religion', models.PositiveIntegerField(choices=[(1, 'Christianity'), (2, 'Islam'), (3, 'Others')], blank=True, null=True)),
                ('permanent_address', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('unique_id', models.UUIDField(editable=False, default=uuid.uuid4, unique=True)),
                ('bank', models.ForeignKey(blank=True, to='students.Bank', null=True)),
                ('country', models.ForeignKey(blank=True, related_name='country_of_residence', to='states.Country', null=True)),
                ('department', models.ForeignKey(to='institutions.Department', null=True)),
                ('faculty', models.ForeignKey(to='institutions.Faculty', null=True)),
                ('institution', models.ForeignKey(blank=True, to='institutions.Institution', null=True)),
                ('lga', models.ForeignKey(verbose_name='LGA', blank=True, related_name='students', to='states.LGA', null=True)),
                ('state_of_origin', models.ForeignKey(blank=True, related_name='students_origin', to='states.State', null=True)),
                ('state_of_residence', models.ForeignKey(blank=True, related_name='students_residence', to='states.State', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='student')),
            ],
            options={
                'verbose_name_plural': 'Students',
                'verbose_name': 'Student',
                'ordering': ('last_name',),
            },
        ),
        migrations.CreateModel(
            name='UniqueMapper',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('reg_number', models.CharField(max_length=30)),
                ('short_institution_name', models.CharField(max_length=5, null=True)),
                ('unique_map', models.CharField(max_length=50, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Unique Mappers',
                'verbose_name': 'Unique Mapper',
                'ordering': ('short_institution_name',),
            },
        ),
        migrations.AddField(
            model_name='scholarship',
            name='student',
            field=models.ForeignKey(blank=True, to='students.Student', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='student',
            field=models.ForeignKey(to='students.Student'),
        ),
    ]
