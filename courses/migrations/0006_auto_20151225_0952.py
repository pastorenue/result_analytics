# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20151126_0807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursedetail',
            name='course',
        ),
        migrations.AddField(
            model_name='course',
            name='unit',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='CourseDetail',
        ),
    ]
