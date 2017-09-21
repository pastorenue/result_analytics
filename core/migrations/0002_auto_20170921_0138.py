# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsetup',
            name='target_cgpa',
            field=models.DecimalField(default=0.0, null=True, decimal_places=2, max_digits=4, blank=True),
        ),
    ]
