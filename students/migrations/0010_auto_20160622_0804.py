# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_auto_20160622_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_status',
            field=models.CharField(null=True, default='A', max_length=1, choices=[('A', 'Active'), ('G', 'Graduated'), ('S', 'Suspended'), ('E', 'Expelled')], blank=True),
        ),
    ]
