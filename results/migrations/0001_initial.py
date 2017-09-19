# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_auto_20170919_1036'),
        ('courses', '0002_course_lecturer'),
        ('students', '0003_auto_20170914_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='CGPA',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('cgpa', models.DecimalField(verbose_name='student_cgpa', decimal_places=2, max_digits=3)),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('level', models.PositiveIntegerField(null=True)),
                ('session', models.CharField(max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(to='students.Student')),
            ],
            options={
                'verbose_name': 'CGPA',
                'verbose_name_plural': 'CGPAs',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Grading',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('caption', models.CharField(max_length=15, null=True)),
                ('grade_points', models.DecimalField(null=True, decimal_places=1, max_digits=2)),
                ('start', models.IntegerField(null=True, default=0)),
                ('end', models.PositiveIntegerField(null=True, default=100)),
                ('institution', models.ForeignKey(to='institutions.Institution', null=True)),
            ],
            options={
                'verbose_name': 'Grading',
                'verbose_name_plural': 'Gradings',
                'ordering': ('caption',),
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('exam_score', models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6)),
                ('assignment_score', models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6)),
                ('quiz_score', models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6)),
                ('total_score', models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6)),
                ('level', models.PositiveIntegerField(null=True, blank=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('credit_load', models.DecimalField(null=True, blank=True, default=0.0, decimal_places=2, max_digits=4)),
                ('session', models.CharField(max_length=10, null=True, blank=True)),
                ('course_load', models.DecimalField(null=True, blank=True, default=0.0, decimal_places=2, max_digits=4)),
                ('date_created', models.DateField(null=True, auto_now_add=True)),
                ('date_modified', models.DateTimeField(null=True, auto_now=True)),
                ('course', models.ForeignKey(to='courses.Course', null=True)),
                ('department', models.ForeignKey(null=True, to='institutions.Department', blank=True)),
                ('student', models.ForeignKey(to='students.Student', null=True)),
            ],
            options={
                'verbose_name': 'Student Result',
                'verbose_name_plural': ' Student Results',
                'ordering': ('-date_created',),
            },
        ),
    ]
