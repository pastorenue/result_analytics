# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_auto_20170919_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='photo',
            field=models.ImageField(upload_to='uploads/%F/%m/%d', null=True),
        ),
    ]
