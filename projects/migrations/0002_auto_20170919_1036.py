# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20170914_1354'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='student',
            field=models.ForeignKey(null=True, to='students.Student', related_name='projects'),
        ),
        migrations.AlterField(
            model_name='projectsupervision',
            name='lecturer',
            field=models.ForeignKey(to='staff.Lecturer', null=True),
        ),
    ]
