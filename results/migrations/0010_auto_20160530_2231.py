# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0009_auto_20160530_2229'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cgpa',
            unique_together=set([]),
        ),
    ]
