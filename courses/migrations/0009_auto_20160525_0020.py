# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_added_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='added_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
