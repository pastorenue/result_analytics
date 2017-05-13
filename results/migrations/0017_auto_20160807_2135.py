# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0016_auto_20160613_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='course_load',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='result',
            name='credit_load',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
