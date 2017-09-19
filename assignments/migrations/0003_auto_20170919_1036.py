# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_quiz_course'),
        ('staff', '0001_initial'),
        ('courses', '0002_course_lecturer'),
        ('students', '0003_auto_20170914_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='invigilators',
            field=models.ManyToManyField(help_text='Hold down the control key and select more than one lecturer', blank=True, to='staff.Lecturer'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='student',
            field=models.ForeignKey(to='students.Student'),
        ),
        migrations.AddField(
            model_name='assignmentscore',
            name='assignment',
            field=models.ForeignKey(to='assignments.Assignment'),
        ),
        migrations.AddField(
            model_name='assignmentscore',
            name='student',
            field=models.ForeignKey(to='students.Student', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(to='courses.Course', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='lecturer',
            field=models.ForeignKey(to='staff.Lecturer', null=True),
        ),
    ]
