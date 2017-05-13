# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0014_auto_20160602_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cgpa',
            name='cgpa',
            field=models.DecimalField(decimal_places=2, verbose_name='student_cgpa', max_digits=3),
        ),
    ]
