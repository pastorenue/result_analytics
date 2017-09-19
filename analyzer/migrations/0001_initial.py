# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actvity',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('activity_name', models.CharField(null=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(to='institutions.Department')),
            ],
            options={
                'ordering': ('date_created',),
                'verbose_name_plural': 'Analysis Activities',
                'verbose_name': 'Analysis Activity',
            },
        ),
    ]
