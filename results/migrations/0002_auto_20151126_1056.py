# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grading',
            name='grade_points',
            field=models.DecimalField(decimal_places=1, max_digits=2, null=True),
        ),
    ]
