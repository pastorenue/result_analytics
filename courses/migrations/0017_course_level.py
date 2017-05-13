# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_course_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.IntegerField(null=True, choices=[(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600)]),
        ),
    ]
