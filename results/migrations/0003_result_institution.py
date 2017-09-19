# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('results', '0002_auto_20170919_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='institution',
            field=models.ForeignKey(null=True, to='institutions.Institution'),
        ),
    ]
