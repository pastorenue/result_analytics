# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('assignment_code', models.UUIDField(editable=False, default=uuid.uuid4, unique=True)),
                ('question_or_instructions', models.TextField()),
                ('level', models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], null=True)),
                ('file', models.FileField(blank=True, upload_to='uploads/assigments/%Y/%m/%d/')),
                ('category', models.CharField(default='mock assignment', choices=[('quiz', 'Quiz'), ('major assignment', 'Major Assignments'), ('mock assignment', 'Mock Assignment')], blank=True, max_length=20)),
                ('standard', models.PositiveIntegerField(default=50, choices=[(80, 'Excellence'), (60, 'Above Average'), (50, 'Average'), (40, 'Fair Enough')], blank=True)),
                ('semester', models.PositiveIntegerField(choices=[(1, 'First Semester'), (2, 'Second Semester')], null=True)),
                ('session', models.CharField(max_length=10, blank=True, null=True)),
                ('possible_points', models.DecimalField(default=0.0, blank=True, max_digits=6, decimal_places=2, null=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('status', models.CharField(default='A', choices=[('A', 'Active'), ('D', 'Declined'), ('S', 'Submitted'), ('M', 'Marked')], max_length=1)),
                ('score', models.DecimalField(default=0.0, decimal_places=2, max_digits=6)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Assignment Grades',
                'verbose_name': 'Assigment Grade',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('score', models.DecimalField(default=0.0, max_digits=6, decimal_places=2, null=True)),
                ('level', models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], blank=True, null=True)),
                ('semester', models.PositiveIntegerField(choices=[(1, 'First Semester'), (2, 'Second Semester')], null=True)),
                ('session', models.CharField(max_length=10, blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Quizes',
                'verbose_name': 'Quiz',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Submitted',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('answer', models.TextField()),
                ('upload_file', models.FileField(blank=True, upload_to='uploads/assignment_answers/%Y/%m/%d')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(to='assignments.Assignment')),
            ],
            options={
                'verbose_name_plural': 'Submitted Assignments',
                'verbose_name': 'Submitted Assignment',
                'ordering': ('-date_created',),
            },
        ),
    ]
