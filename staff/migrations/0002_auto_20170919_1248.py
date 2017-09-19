# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lecturer',
            options={'permissions': (('can_edit_records', 'Staff can edit other records'), ('is_admin', 'Staff is an administrative user'), ('can_add_courses', 'Staff can add new courses'), ('can_add_result', 'Staff can add results')), 'verbose_name_plural': 'Lecturers', 'ordering': ('first_name',), 'verbose_name': 'Lecturer'},
        ),
        migrations.AddField(
            model_name='lecturer',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
