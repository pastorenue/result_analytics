# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20170914_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('assignment_code', models.UUIDField(unique=True, default=uuid.uuid4, editable=False)),
                ('question_or_instructions', models.TextField()),
                ('level', models.PositiveIntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('file', models.FileField(blank=True, upload_to='uploads/assigments/%Y/%m/%d/')),
                ('category', models.CharField(max_length=20, choices=[('quiz', 'Quiz'), ('major assignment', 'Major Assignments'), ('mock assignment', 'Mock Assignment')], blank=True, default='mock assignment')),
                ('standard', models.PositiveIntegerField(choices=[(80, 'Excellence'), (60, 'Above Average'), (50, 'Average'), (40, 'Fair Enough')], blank=True, default=50)),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('session', models.CharField(max_length=10, null=True, blank=True)),
                ('possible_points', models.DecimalField(null=True, blank=True, default=0.0, decimal_places=2, max_digits=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='AssignmentScore',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', models.CharField(max_length=1, choices=[('A', 'Active'), ('D', 'Declined'), ('S', 'Submitted'), ('M', 'Marked')], default='A')),
                ('score', models.DecimalField(default=0.0, decimal_places=2, max_digits=6)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Assigment Grade',
                'verbose_name_plural': 'Assignment Grades',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('score', models.DecimalField(null=True, default=0.0, decimal_places=2, max_digits=6)),
                ('level', models.PositiveIntegerField(null=True, blank=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('session', models.CharField(max_length=10, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizes',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Submitted',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('answer', models.TextField()),
                ('upload_file', models.FileField(blank=True, upload_to='uploads/assignment_answers/%Y/%m/%d')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(to='assignments.Assignment')),
                ('student', models.ForeignKey(to='students.Student')),
            ],
            options={
                'verbose_name': 'Submitted Assignment',
                'verbose_name_plural': 'Submitted Assignments',
                'ordering': ('-date_created',),
            },
        ),
    ]
