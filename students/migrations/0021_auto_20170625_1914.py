# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0020_student_year_of_admission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='attached_file',
            field=models.FileField(upload_to='uploads/docs/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
