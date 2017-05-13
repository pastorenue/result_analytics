# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0013_auto_20160531_0701'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'verbose_name': 'Student Result', 'verbose_name_plural': ' Student Results', 'ordering': ('-date_created',)},
        ),
    ]
