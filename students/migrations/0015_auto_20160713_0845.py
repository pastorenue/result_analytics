# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_auto_20160713_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholarship',
            name='student',
        ),
        migrations.AddField(
            model_name='scholarship',
            name='student',
            field=models.ManyToManyField(blank=True, to='students.Student', null=True, related_name='scholarship'),
        ),
    ]
