# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('students', '0003_auto_20170914_1354'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('course_code', models.CharField(max_length=7, null=True)),
                ('name', models.CharField(max_length=250, null=True)),
                ('unit', models.PositiveIntegerField(verbose_name='Number of credit units', default=0)),
                ('level', models.IntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('semester', models.IntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('date_created', models.DateTimeField(null=True, auto_now_add=True)),
                ('date_modified', models.DateTimeField(null=True, auto_now=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(to='institutions.Department', null=True)),
            ],
            options={
                'verbose_name': 'Course Available',
                'verbose_name_plural': 'Courses Available',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('level', models.PositiveIntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('session', models.CharField(max_length=15, null=True)),
                ('carried_over', models.NullBooleanField(default=False)),
                ('date_created', models.DateField(null=True, auto_now_add=True)),
                ('course', models.ManyToManyField(to='courses.Course')),
                ('department', models.ForeignKey(to='institutions.Department', null=True)),
                ('student', models.ForeignKey(to='students.Student', null=True)),
            ],
            options={
                'verbose_name': 'Course Registered',
                'verbose_name_plural': 'Courses Registered',
                'ordering': ('level',),
            },
        ),
    ]
