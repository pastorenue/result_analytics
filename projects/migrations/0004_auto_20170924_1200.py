# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_supervisor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='student',
            field=models.ForeignKey(to='students.Student', null=True),
        ),
    ]
