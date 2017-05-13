# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0018_result_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='course_load',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='result',
            name='credit_load',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True, default=0.0),
        ),
    ]
