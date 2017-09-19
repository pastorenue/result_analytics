# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0001_initial'),
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actvity',
            name='results',
            field=models.ForeignKey(to='results.Result'),
        ),
    ]
