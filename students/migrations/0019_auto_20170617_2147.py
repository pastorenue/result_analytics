# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0018_auto_20160722_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='year_of_graduation',
            new_name='course_duration',
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(upload_to='uploads', blank=True),
        ),
    ]
