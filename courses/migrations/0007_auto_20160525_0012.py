# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20151225_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='date_modified',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
    ]
