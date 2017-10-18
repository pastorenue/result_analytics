# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_lecturer_photo'),
        ('results', '0003_result_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='modified_by',
            field=models.ForeignKey(to='staff.Lecturer', null=True, blank=True),
        ),
    ]
