# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_department_id_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeparmentalCode',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(null=True, max_length=50)),
                ('code', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Departmental Codes',
                'verbose_name': 'Departmental Code',
                'ordering': ('name',),
            },
        ),
    ]
