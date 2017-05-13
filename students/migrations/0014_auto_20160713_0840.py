# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_auto_20160713_0703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='number',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='category',
        ),
        migrations.AddField(
            model_name='student',
            name='phone_number',
            field=models.CharField(blank=True, null=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, null=True, max_length=100),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='PhoneNumber',
        ),
    ]
