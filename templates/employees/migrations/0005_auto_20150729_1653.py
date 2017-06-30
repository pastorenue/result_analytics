# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_auto_20150729_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uid',
            field=models.SlugField(default=b'2ed3afa761d34df2b9c6ead871d08959', max_length=32, editable=False),
        ),
    ]
