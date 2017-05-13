# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20151113_0940'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('caption', models.CharField(max_length=15, null=True)),
                ('grade_points', models.IntegerField(null=True)),
                ('start', models.IntegerField(default=0, null=True)),
                ('end', models.PositiveIntegerField(default=100, null=True)),
            ],
            options={
                'verbose_name': 'Grading',
                'ordering': ('caption',),
                'verbose_name_plural': 'Gradings',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('score', models.DecimalField(max_digits=6, decimal_places=2, default=0.0, null=True)),
                ('level', models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], null=True)),
                ('semester', models.PositiveIntegerField(choices=[(1, 'First Semester'), (2, 'Second Semester')], null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('course', models.ForeignKey(to='courses.CourseRegistration', null=True)),
                ('student', models.ForeignKey(to='students.Student', null=True)),
            ],
            options={
                'verbose_name': 'Student Result',
                'ordering': ('date_created',),
                'verbose_name_plural': ' Student Results',
            },
        ),
    ]
