# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        ('institutions', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseregistration',
            name='student',
            field=models.ForeignKey(null=True, to='students.Student'),
        ),
        migrations.AddField(
            model_name='coursedetail',
            name='course',
            field=models.ForeignKey(null=True, to='courses.Course'),
        ),
        migrations.AddField(
            model_name='coursedetail',
            name='course_registered',
            field=models.ForeignKey(null=True, to='courses.CourseRegistration'),
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(null=True, to='institutions.Department'),
        ),
        migrations.AddField(
            model_name='course',
            name='lecturer',
            field=models.ForeignKey(null=True, blank=True, related_name='courses', to='institutions.Lecturer'),
        ),
    ]
