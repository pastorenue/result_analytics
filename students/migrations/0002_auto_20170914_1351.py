# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='lga',
        ),
        migrations.RemoveField(
            model_name='student',
            name='unique_id',
        ),
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='program_type',
            field=models.PositiveIntegerField(choices=[(1, 'Regular'), (2, 'Sandwich'), (3, 'CEP'), (4, 'Diploma'), (5, 'Others')], blank=True, null=True),
        ),
    ]
