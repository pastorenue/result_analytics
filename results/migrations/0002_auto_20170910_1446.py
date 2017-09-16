# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('students', '0001_initial'),
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='student',
            field=models.ForeignKey(to='students.Student', null=True),
        ),
        migrations.AddField(
            model_name='grading',
            name='institution',
            field=models.ForeignKey(to='institutions.Institution', null=True),
        ),
        migrations.AddField(
            model_name='cgpa',
            name='student',
            field=models.ForeignKey(to='students.Student'),
        ),
    ]
