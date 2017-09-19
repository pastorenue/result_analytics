# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('course_code', models.CharField(null=True, max_length=7)),
                ('name', models.CharField(null=True, max_length=250)),
                ('unit', models.PositiveIntegerField(verbose_name='Number of credit units', default=0)),
                ('level', models.IntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('semester', models.IntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Courses Available',
                'verbose_name': 'Course Available',
            },
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('level', models.PositiveIntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('session', models.CharField(null=True, max_length=15)),
                ('carried_over', models.NullBooleanField(default=False)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('course', models.ManyToManyField(to='courses.Course')),
                ('department', models.ForeignKey(to='institutions.Department', null=True)),
            ],
            options={
                'ordering': ('level',),
                'verbose_name_plural': 'Courses Registered',
                'verbose_name': 'Course Registered',
            },
        ),
    ]
