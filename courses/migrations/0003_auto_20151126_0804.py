# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20151113_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursedetail',
            name='carried_over',
        ),
        migrations.RemoveField(
            model_name='coursedetail',
            name='course_registered',
        ),
        migrations.AddField(
            model_name='courseregistration',
            name='carried_over',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='courseregistration',
            name='course',
            field=models.ForeignKey(to='courses.Course', null=True),
        ),
    ]
