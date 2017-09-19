# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CGPA',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('cgpa', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='student_cgpa')),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('level', models.PositiveIntegerField(null=True)),
                ('session', models.CharField(max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name_plural': 'CGPAs',
                'verbose_name': 'CGPA',
            },
        ),
        migrations.CreateModel(
            name='Grading',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('caption', models.CharField(null=True, max_length=15)),
                ('grade_points', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('start', models.IntegerField(null=True, default=0)),
                ('end', models.PositiveIntegerField(null=True, default=100)),
            ],
            options={
                'ordering': ('caption',),
                'verbose_name_plural': 'Gradings',
                'verbose_name': 'Grading',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('exam_score', models.DecimalField(decimal_places=2, max_digits=6, null=True, default=0.0)),
                ('assignment_score', models.DecimalField(decimal_places=2, max_digits=6, null=True, default=0.0)),
                ('quiz_score', models.DecimalField(decimal_places=2, max_digits=6, null=True, default=0.0)),
                ('total_score', models.DecimalField(decimal_places=2, max_digits=6, null=True, default=0.0)),
                ('level', models.PositiveIntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], blank=True)),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('credit_load', models.DecimalField(decimal_places=2, max_digits=4, null=True, default=0.0, blank=True)),
                ('session', models.CharField(blank=True, null=True, max_length=10)),
                ('course_load', models.DecimalField(decimal_places=2, max_digits=4, null=True, default=0.0, blank=True)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('course', models.ForeignKey(to='courses.Course', null=True)),
                ('department', models.ForeignKey(to='institutions.Department', null=True, blank=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name_plural': ' Student Results',
                'verbose_name': 'Student Result',
            },
        ),
    ]
