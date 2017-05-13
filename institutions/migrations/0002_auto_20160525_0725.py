# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='title',
            field=models.CharField(max_length=5, choices=[('Mr.', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr.', 'Dr'), ('Prof', 'Prof'), ('Prof', 'Mallam')], null=True, blank=True),
        ),
    ]
