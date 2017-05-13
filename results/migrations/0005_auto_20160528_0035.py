# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_auto_20160525_0703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cgpa',
            name='level',
        ),
        migrations.AlterField(
            model_name='cgpa',
            name='semester',
            field=models.PositiveIntegerField(choices=[(1, 'First Semester'), (2, 'Second Semester')], null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='level',
            field=models.PositiveIntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], blank=True),
        ),
    ]
