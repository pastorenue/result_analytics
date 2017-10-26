# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20171017_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseregistration',
            name='course',
        ),
        migrations.AddField(
            model_name='courseregistration',
            name='course',
            field=models.ForeignKey(null=True, to='courses.Course'),
        ),
    ]
