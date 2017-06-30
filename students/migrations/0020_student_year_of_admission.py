# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0019_auto_20170617_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='year_of_admission',
            field=models.DateField(default=datetime.datetime(2017, 6, 17, 20, 58, 36, 292318, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
