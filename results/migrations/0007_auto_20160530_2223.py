# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_cgpa_level'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cgpa',
            options={'verbose_name': 'CGPA', 'verbose_name_plural': 'CGPAs'},
        ),
        migrations.AlterField(
            model_name='cgpa',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
