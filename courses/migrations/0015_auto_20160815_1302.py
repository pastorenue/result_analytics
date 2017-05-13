# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_auto_20160814_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lecturer',
            field=models.ManyToManyField(to='institutions.Lecturer', help_text='Hold down the control key and select more than one lecturer', blank=True),
        ),
    ]
