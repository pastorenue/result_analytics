# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20160622_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_status',
            field=models.PositiveSmallIntegerField(default=0, blank=True, choices=[(0, 'Active'), (1, 'Graduated'), (2, 'Suspended'), (3, 'Expelled')], null=True),
        ),
    ]
