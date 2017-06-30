# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20150731_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uid',
            field=models.SlugField(default=b'4713c0e7ec54469383ed6678554edeef', max_length=32, editable=False),
        ),
    ]
