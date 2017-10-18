# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0003_assignment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='category',
            field=models.CharField(max_length=20, default='mock assignment', choices=[('major assignment', 'Major Assignments'), ('mock assignment', 'Mock Assignment')], blank=True),
        ),
    ]
