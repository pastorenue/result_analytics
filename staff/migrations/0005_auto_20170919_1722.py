# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20170919_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='slug',
            field=models.SlugField(unique=True, blank=True, max_length=250, null=True),
        ),
    ]
