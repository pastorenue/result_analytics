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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('activity_name', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(to='institutions.Department')),
            ],
            options={
                'verbose_name_plural': 'Analysis Activities',
                'verbose_name': 'Analysis Activity',
                'ordering': ('date_created',),
            },
        ),
    ]
