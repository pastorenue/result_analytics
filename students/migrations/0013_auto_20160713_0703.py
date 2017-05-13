# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_auto_20160713_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='students',
            field=models.ForeignKey(to='students.Student'),
        ),
    ]
