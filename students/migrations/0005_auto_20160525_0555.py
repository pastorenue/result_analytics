# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20160525_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='religion',
            field=models.PositiveIntegerField(null=True, blank=True, choices=[(1, 'Christianity'), (2, 'Islam'), (3, 'Others')]),
        ),
    ]
