# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_auto_20150729_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uid',
            field=models.SlugField(default=b'ae66d9b550584fbcb04403f70b433853', max_length=32, editable=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(related_name='employee', to=settings.AUTH_USER_MODEL),
        ),
    ]
