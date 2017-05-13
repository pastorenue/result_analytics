# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20160525_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.ForeignKey(blank=True, to='students.Address', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(verbose_name='First name', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(verbose_name='Surname', max_length=50, null=True),
        ),
    ]
