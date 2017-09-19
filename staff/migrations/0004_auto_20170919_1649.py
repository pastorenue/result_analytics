# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_auto_20170919_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='slug',
            field=models.SlugField(blank=True, unique=True, null=True),
        ),
    ]
