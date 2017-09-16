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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('course_code', models.CharField(max_length=7, null=True)),
                ('name', models.CharField(max_length=250, null=True)),
                ('unit', models.PositiveIntegerField(default=0, verbose_name='Number of credit units')),
                ('level', models.IntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], null=True)),
                ('semester', models.IntegerField(choices=[(1, 'First Semester'), (2, 'Second Semester')], null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Courses Available',
                'verbose_name': 'Course Available',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('level', models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], null=True)),
                ('semester', models.PositiveIntegerField(choices=[(1, 'First Semester'), (2, 'Second Semester')], null=True)),
                ('session', models.CharField(max_length=15, null=True)),
                ('carried_over', models.NullBooleanField(default=False)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('course', models.ManyToManyField(to='courses.Course')),
                ('department', models.ForeignKey(to='institutions.Department', null=True)),
            ],
            options={
                'verbose_name_plural': 'Courses Registered',
                'verbose_name': 'Course Registered',
                'ordering': ('level',),
            },
        ),
    ]
