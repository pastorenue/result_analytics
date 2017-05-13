# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20160811_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lecturer',
            field=models.ManyToManyField(blank=True, to='institutions.Lecturer'),
        ),
    ]
