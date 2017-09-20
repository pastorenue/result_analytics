# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_auto_20170919_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='status',
            field=models.CharField(default='A', max_length=1, choices=[('A', 'Active'), ('D', 'Deactivated')]),
        ),
    ]
