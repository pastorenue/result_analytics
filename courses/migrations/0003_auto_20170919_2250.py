# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20170919_1122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='lecturer',
            new_name='lecturers',
        ),
    ]
