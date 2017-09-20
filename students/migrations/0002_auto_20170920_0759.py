# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='institution',
            field=models.ForeignKey(null=True, to='institutions.Institution'),
        ),
        migrations.AlterField(
            model_name='student',
            name='sex',
            field=models.CharField(null=True, max_length=1, choices=[('M', 'Male'), ('F', 'Female')]),
        ),
    ]
