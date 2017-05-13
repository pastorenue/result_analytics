# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20160628_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseregistration',
            name='course',
            field=models.ManyToManyField(to='courses.Course'),
        ),
    ]
