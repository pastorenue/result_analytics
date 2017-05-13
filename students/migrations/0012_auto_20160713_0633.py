# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20160713_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
    ]
