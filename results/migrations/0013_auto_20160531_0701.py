# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0012_auto_20160530_2235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cgpa',
            options={'ordering': ('-date_created',), 'verbose_name': 'CGPA', 'verbose_name_plural': 'CGPAs'},
        ),
    ]
