# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0015_auto_20160713_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='student',
            field=models.ManyToManyField(to='students.Student', related_name='scholarship', blank=True),
        ),
    ]
