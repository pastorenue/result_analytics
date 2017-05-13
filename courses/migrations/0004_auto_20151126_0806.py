# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20151126_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseregistration',
            name='carried_over',
            field=models.BooleanField(default=False),
        ),
    ]
