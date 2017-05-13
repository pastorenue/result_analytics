# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_auto_20150728_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uid',
            field=models.SlugField(default=b'37fde6e560304fa08839668c2185b856', max_length=32, editable=False),
        ),
    ]
