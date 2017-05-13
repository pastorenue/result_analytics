# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_auto_20150729_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uid',
            field=models.SlugField(default=b'279252cb2dac481a92e9b90dc7653ce2', max_length=32, editable=False),
        ),
    ]
