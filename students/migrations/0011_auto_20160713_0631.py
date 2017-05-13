# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_auto_20160622_0804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='file',
            new_name='attached_file',
        ),
        migrations.RemoveField(
            model_name='document',
            name='ctype',
        ),
        migrations.RemoveField(
            model_name='document',
            name='object_id',
        ),
        migrations.AlterField(
            model_name='document',
            name='students',
            field=models.ForeignKey(related_name='documents', to='students.Student'),
        ),
    ]
