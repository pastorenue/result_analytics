# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0016_auto_20160715_0137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='attached_file',
            new_name='file',
        ),
    ]
