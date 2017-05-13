# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20160525_0020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='code',
            new_name='course_code',
        ),
    ]
