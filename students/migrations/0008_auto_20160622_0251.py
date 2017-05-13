# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_auto_20160608_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_status',
            field=models.CharField(max_length=1, blank=True, default=0, null=True, choices=[(0, 'Active'), (1, 'Graduated'), (2, 'Suspended'), (3, 'Expelled')]),
        ),
    ]
