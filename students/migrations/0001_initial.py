# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('states', '0001_initial'),
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=150)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('attached_file', models.FileField(upload_to='uploads/docs/%Y/%m/%d/')),
                ('name', models.CharField(blank=True, null=True, max_length=255)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True, max_length=30)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Phone Categories',
                'verbose_name': 'Phone Category',
            },
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, null=True, max_length=250)),
                ('provider', models.CharField(blank=True, null=True, max_length=250)),
                ('location', models.CharField(blank=True, null=True, max_length=150)),
                ('website', models.URLField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name_plural': 'Scholarships',
                'verbose_name': 'Scholarship',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='uploads')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('last_name', models.CharField(null=True, verbose_name='Surname', max_length=50)),
                ('first_name', models.CharField(null=True, verbose_name='First name', max_length=50)),
                ('middle_name', models.CharField(blank=True, verbose_name='Middle name', max_length=50)),
                ('user_status', models.CharField(blank=True, null=True, choices=[('A', 'Active'), ('G', 'Graduated'), ('S', 'Suspended'), ('E', 'Expelled')], default='A', max_length=1)),
                ('reg_number', models.CharField(max_length=30)),
                ('bank_account_number', models.CharField(blank=True, null=True, max_length=20)),
                ('marital_status', models.PositiveSmallIntegerField(null=True, choices=[(1, 'Single'), (2, 'Married'), (3, 'Widowed'), (4, 'Divorced')], blank=True)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('level', models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], blank=True)),
                ('program_type', models.PositiveIntegerField(null=True, choices=[(1, 'Regular'), (2, 'Sandwich'), (3, 'CEP'), (4, 'Diploma'), (5, 'Others')], blank=True)),
                ('birth_date', models.DateField(null=True, db_index=True, blank=True)),
                ('library_id_number', models.PositiveIntegerField(null=True, blank=True)),
                ('school_id_number', models.PositiveIntegerField(null=True, blank=True)),
                ('address', models.CharField(blank=True, null=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, null=True, max_length=15)),
                ('date_gained_admission', models.DateField(auto_now=True)),
                ('blood_group', models.CharField(blank=True, choices=[('A', 'A'), ('AB', 'AB'), ('B', 'B'), ('O+', 'O+'), ('O-', 'O-')], max_length=2)),
                ('genotype', models.CharField(blank=True, choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS')], max_length=2)),
                ('national_id_number', models.CharField(blank=True, verbose_name='National ID Number', max_length=50)),
                ('year_of_admission', models.DateField()),
                ('course_duration', models.PositiveIntegerField()),
                ('religion', models.PositiveIntegerField(null=True, choices=[(1, 'Christianity'), (2, 'Islam'), (3, 'Others')], blank=True)),
                ('permanent_address', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('bank', models.ForeignKey(to='students.Bank', null=True, blank=True)),
                ('country', models.ForeignKey(to='states.Country', null=True, related_name='country_of_residence', blank=True)),
                ('department', models.ForeignKey(to='institutions.Department', null=True)),
                ('faculty', models.ForeignKey(to='institutions.Faculty', null=True)),
                ('institution', models.ForeignKey(to='institutions.Institution', null=True, blank=True)),
                ('state_of_origin', models.ForeignKey(to='states.State', null=True, related_name='students_origin', blank=True)),
                ('state_of_residence', models.ForeignKey(to='states.State', null=True, related_name='students_residence', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='student')),
            ],
            options={
                'ordering': ('last_name',),
                'verbose_name_plural': 'Students',
                'verbose_name': 'Student',
            },
        ),
        migrations.CreateModel(
            name='UniqueMapper',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('reg_number', models.CharField(max_length=30)),
                ('short_institution_name', models.CharField(null=True, max_length=5)),
                ('unique_map', models.CharField(blank=True, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('short_institution_name',),
                'verbose_name_plural': 'Unique Mappers',
                'verbose_name': 'Unique Mapper',
            },
        ),
        migrations.AddField(
            model_name='scholarship',
            name='student',
            field=models.ForeignKey(to='students.Student', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='student',
            field=models.ForeignKey(to='students.Student'),
        ),
    ]
