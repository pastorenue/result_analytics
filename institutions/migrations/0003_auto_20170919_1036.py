# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20170919_1036'),
        ('institutions', '0002_auto_20170919_1036'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Lecturer',
        ),
        migrations.DeleteModel(
            name='Position',
        ),
    ]
