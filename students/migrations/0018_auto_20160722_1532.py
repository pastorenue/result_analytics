# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0017_auto_20160717_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='file',
        ),
        migrations.AddField(
            model_name='document',
            name='attached_file',
            field=models.FileField(default=datetime.datetime(2016, 7, 22, 14, 32, 19, 687819, tzinfo=utc), upload_to='students/docs/%Y/%m/%d/'),
            preserve_default=False,
        ),
    ]
