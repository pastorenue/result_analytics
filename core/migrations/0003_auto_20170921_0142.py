# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170921_0138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentsetup',
            old_name='recommed_my_help_to_students',
            new_name='recommend_my_help_to_students',
        ),
    ]
