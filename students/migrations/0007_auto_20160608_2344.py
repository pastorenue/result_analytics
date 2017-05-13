# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20160528_0035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scholarship',
            options={'ordering': ('title',), 'verbose_name_plural': 'Scholarships', 'verbose_name': 'Scholarship'},
        ),
        migrations.RenameField(
            model_name='scholarship',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='scholarship',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 22, 44, 2, 822800, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scholarship',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 6, 8, 22, 44, 13, 888100, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
