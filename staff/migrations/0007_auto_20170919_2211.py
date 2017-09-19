# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_auto_20170919_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='marital_status',
            field=models.CharField(null=True, max_length=2, choices=[('S', 'Single'), ('M', 'Married'), ('W', 'Widowed'), ('D', 'Divorced')], blank=True),
        ),
    ]
