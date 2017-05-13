# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=7, null=True)),
                ('name', models.CharField(max_length=250, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Courses Available',
                'verbose_name': 'Course Available',
            },
        ),
        migrations.CreateModel(
            name='CourseDetail',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('unit', models.PositiveIntegerField(default=0)),
                ('carried_over', models.NullBooleanField(default=False)),
            ],
            options={
                'ordering': ('course',),
                'verbose_name_plural': 'Courses Details',
                'verbose_name': 'Course Details',
            },
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('level', models.PositiveIntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)])),
                ('semester', models.PositiveIntegerField(null=True, choices=[(1, 'First Semester'), (2, 'Second Semester')])),
                ('session', models.CharField(max_length=15, null=True)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('department', models.ForeignKey(null=True, to='institutions.Department')),
            ],
            options={
                'ordering': ('level',),
                'verbose_name_plural': 'Courses Registered',
                'verbose_name': 'Course Registered',
            },
        ),
    ]
