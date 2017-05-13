# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0003_auto_20160525_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cgpa',
            name='cgpa',
            field=models.DecimalField(verbose_name='cgpa', max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='result',
            name='course',
            field=models.ForeignKey(null=True, to='courses.Course'),
        ),
    ]
