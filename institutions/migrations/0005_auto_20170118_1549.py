# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0004_deparmentalcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='id_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
