# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0015_auto_20160608_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='level',
            field=models.PositiveIntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)], blank=True),
        ),
    ]
