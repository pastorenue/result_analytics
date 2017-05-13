# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0017_auto_20160807_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='session',
            field=models.CharField(max_length=10, blank=True, null=True),
        ),
    ]
