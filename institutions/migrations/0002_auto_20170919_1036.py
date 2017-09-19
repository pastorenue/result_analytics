# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturer',
            name='department',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='position',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='position',
            name='reports_to',
        ),
    ]
