# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20151114_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_status',
            field=models.CharField(max_length=1, choices=[('B', 'Barred'), ('A', 'Active'), ('G', 'Inactive')], null=True, blank=True),
        ),
    ]
