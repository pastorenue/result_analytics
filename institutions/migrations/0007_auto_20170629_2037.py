# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0006_lecturer_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ('name',), 'verbose_name': 'Department', 'verbose_name_plural': 'Departments'},
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
