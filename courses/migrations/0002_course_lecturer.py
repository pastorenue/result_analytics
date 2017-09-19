# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='lecturer',
            field=models.ManyToManyField(help_text='Hold down the control key and select more than one lecturer', blank=True, to='staff.Lecturer'),
        ),
    ]
