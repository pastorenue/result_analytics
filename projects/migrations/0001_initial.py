# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(null=True, max_length=250)),
                ('description', models.TextField(null=True, blank=True)),
                ('category', models.CharField(null=True, max_length=50)),
                ('file', models.FileField(blank=True, upload_to='students/projects/%Y/%m/%d/')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
                ('tag', models.CharField(blank=True, null=True, max_length=150)),
                ('slug', models.SlugField(unique=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Student Projects',
                'verbose_name': 'Student Project',
            },
        ),
    ]
