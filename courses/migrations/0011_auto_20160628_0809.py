# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20160525_0731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseregistration',
            name='course',
        ),
        migrations.AddField(
            model_name='courseregistration',
            name='course',
            field=models.ManyToManyField(to='courses.Course', null=True),
        ),
    ]
