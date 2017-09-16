# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcadamicYear',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('year_starting', models.DateField()),
                ('year_ending', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AdminStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=3, null=True)),
                ('id_number', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Departments',
                'verbose_name': 'Department',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='DepartmentalCode',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('code', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Departmental Codes',
                'verbose_name': 'Departmental Code',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=5, null=True)),
                ('name', models.CharField(max_length=250, null=True)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
                'verbose_name': 'Faculty',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=250, null=True)),
                ('location', models.CharField(max_length=150, blank=True, null=True)),
                ('logo', models.ImageField(blank=True, upload_to='institution/logo/%Y/%m/')),
                ('postal_code', models.CharField(max_length=30, blank=True, null=True)),
                ('full_address', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Institutions',
                'verbose_name': 'Institution',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=5, choices=[('Mr.', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr.', 'Dr'), ('Prof', 'Prof'), ('Mallam', 'Mallam')], blank=True, null=True)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('specialty', models.CharField(max_length=170, blank=True, null=True)),
                ('unique_id', models.UUIDField(editable=False, default=uuid.uuid4, unique=True)),
                ('slug', models.SlugField(unique=True, null=True)),
                ('department', models.ForeignKey(to='institutions.Department', null=True)),
                ('institution', models.ForeignKey(to='institutions.Institution', null=True)),
            ],
            options={
                'verbose_name_plural': 'Lecturers',
                'verbose_name': 'Lecturer',
                'ordering': ('first_name',),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('reports_to', models.ForeignKey(blank=True, related_name='reports', to='institutions.Position', null=True)),
            ],
            options={
                'verbose_name_plural': 'Positions',
                'verbose_name': 'Position',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='lecturer',
            name='position',
            field=models.ForeignKey(blank=True, to='institutions.Position', null=True),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='lecturer'),
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(to='institutions.Faculty', related_name='department', null=True),
        ),
        migrations.AddField(
            model_name='adminstaff',
            name='institution',
            field=models.OneToOneField(to='institutions.Institution'),
        ),
        migrations.AddField(
            model_name='adminstaff',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
