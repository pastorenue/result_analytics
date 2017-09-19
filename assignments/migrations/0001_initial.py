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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('assignment_code', models.UUIDField(unique=True, editable=False, default=uuid.uuid4)),
                ('question_or_instructions', models.TextField()),
                ('level', models.PositiveIntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('file', models.FileField(blank=True, upload_to='uploads/assigments/%Y/%m/%d/')),
                ('category', models.CharField(blank=True, choices=[('quiz', 'Quiz'), ('major assignment', 'Major Assignments'), ('mock assignment', 'Mock Assignment')], default='mock assignment', max_length=20)),
                ('standard', models.PositiveIntegerField(choices=[(80, 'Excellence'), (60, 'Above Average'), (50, 'Average'), (40, 'Fair Enough')], default=50, blank=True)),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('session', models.CharField(blank=True, null=True, max_length=10)),
                ('possible_points', models.DecimalField(decimal_places=2, max_digits=6, null=True, default=0.0, blank=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Declined'), ('S', 'Submitted'), ('M', 'Marked')], default='A', max_length=1)),
                ('score', models.DecimalField(decimal_places=2, max_digits=6, default=0.0)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name_plural': 'Assignment Grades',
                'verbose_name': 'Assigment Grade',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=6, null=True, default=0.0)),
                ('level', models.PositiveIntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], blank=True)),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('session', models.CharField(blank=True, null=True, max_length=10)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name_plural': 'Quizes',
                'verbose_name': 'Quiz',
            },
        ),
        migrations.CreateModel(
            name='Submitted',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('answer', models.TextField()),
                ('upload_file', models.FileField(blank=True, upload_to='uploads/assignment_answers/%Y/%m/%d')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(to='assignments.Assignment')),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name_plural': 'Submitted Assignments',
                'verbose_name': 'Submitted Assignment',
            },
        ),
    ]
