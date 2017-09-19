# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseregistration',
            name='student',
            field=models.ForeignKey(to='students.Student', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='added_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(to='institutions.Department', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='lecturer',
            field=models.ManyToManyField(to='staff.Lecturer', blank=True, help_text='Hold down the control key and select more than one lecturer'),
        ),
    ]
