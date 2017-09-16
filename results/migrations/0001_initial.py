# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CGPA',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('cgpa', models.DecimalField(max_digits=3, verbose_name='student_cgpa', decimal_places=2)),
                ('semester', models.PositiveIntegerField(choices=[(1, 'First Semester'), (2, 'Second Semester')], null=True)),
                ('level', models.PositiveIntegerField(null=True)),
                ('session', models.CharField(max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'CGPAs',
                'verbose_name': 'CGPA',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Grading',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('caption', models.CharField(max_length=15, null=True)),
                ('grade_points', models.DecimalField(max_digits=2, decimal_places=1, null=True)),
                ('start', models.IntegerField(default=0, null=True)),
                ('end', models.PositiveIntegerField(default=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Gradings',
                'verbose_name': 'Grading',
                'ordering': ('caption',),
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('exam_score', models.DecimalField(default=0.0, max_digits=6, decimal_places=2, null=True)),
                ('assignment_score', models.DecimalField(default=0.0, max_digits=6, decimal_places=2, null=True)),
                ('quiz_score', models.DecimalField(default=0.0, max_digits=6, decimal_places=2, null=True)),
                ('total_score', models.DecimalField(default=0.0, max_digits=6, decimal_places=2, null=True)),
                ('level', models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], blank=True, null=True)),
                ('semester', models.PositiveIntegerField(choices=[(1, 'First Semester'), (2, 'Second Semester')], null=True)),
                ('credit_load', models.DecimalField(default=0.0, blank=True, max_digits=4, decimal_places=2, null=True)),
                ('session', models.CharField(max_length=10, blank=True, null=True)),
                ('course_load', models.DecimalField(default=0.0, blank=True, max_digits=4, decimal_places=2, null=True)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('course', models.ForeignKey(to='courses.Course', null=True)),
                ('department', models.ForeignKey(blank=True, to='institutions.Department', null=True)),
            ],
            options={
                'verbose_name_plural': ' Student Results',
                'verbose_name': 'Student Result',
                'ordering': ('-date_created',),
            },
        ),
    ]
