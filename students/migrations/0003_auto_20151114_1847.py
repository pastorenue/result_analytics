# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20151114_1838'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Student Adddresses', 'ordering': ('number',), 'verbose_name': 'Student Address'},
        ),
    ]
