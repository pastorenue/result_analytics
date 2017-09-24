# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_lecturer_photo'),
        ('projects', '0002_project_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='supervisor',
            field=models.ForeignKey(null=True, blank=True, to='staff.Lecturer'),
        ),
    ]
