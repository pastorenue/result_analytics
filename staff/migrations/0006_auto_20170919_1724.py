# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_auto_20170919_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='gender',
            field=models.CharField(null=True, max_length=2, choices=[('M', 'Male'), ('F', 'Female')]),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='marital_status',
            field=models.CharField(null=True, max_length=2, choices=[(1, 'Single'), (2, 'Married'), (3, 'Widowed'), (4, 'Divorced')], blank=True),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='title',
            field=models.CharField(null=True, max_length=20, choices=[('Mr.', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr.', 'Dr'), ('Prof', 'Prof'), ('Mallam', 'Mallam')], blank=True),
        ),
    ]
