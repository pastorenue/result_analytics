# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import river.models.fields.state


class Migration(migrations.Migration):

    dependencies = [
        ('river', '0008_auto_20161017_0916'),
        ('students', '0021_auto_20170625_1914'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ('last_name',), 'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AddField(
            model_name='student',
            name='clearance_status',
            field=river.models.fields.state.StateField(null=True, blank=True, editable=False, to='river.State'),
        ),
    ]
