# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_auto_20160525_0725'),
        ('courses', '0012_auto_20160715_0138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='lecturer',
        ),
        migrations.AddField(
            model_name='course',
            name='lecturer',
            field=models.ManyToManyField(blank=True, to='institutions.Lecturer', related_name='courses'),
        ),
    ]
