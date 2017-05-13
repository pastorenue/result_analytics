# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0005_auto_20170118_1549'),
        ('results', '0019_auto_20160814_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actvity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('activity_name', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(to='institutions.Department')),
                ('results', models.ForeignKey(to='results.Result')),
            ],
            options={
                'verbose_name': 'Analysis Activity',
                'verbose_name_plural': 'Analysis Activities',
                'ordering': ('date_created',),
            },
        ),
    ]
