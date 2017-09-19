# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20170919_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectsupervision',
            name='lecturer',
        ),
        migrations.RemoveField(
            model_name='projectsupervision',
            name='project',
        ),
        migrations.DeleteModel(
            name='ProjectSupervision',
        ),
    ]
