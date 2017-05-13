# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_auto_20160528_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='cgpa',
            name='level',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
