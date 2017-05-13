# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20151126_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseregistration',
            name='carried_over',
            field=models.NullBooleanField(default=False),
        ),
    ]
