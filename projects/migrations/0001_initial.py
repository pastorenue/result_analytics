# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=250, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(max_length=50, null=True)),
                ('file', models.FileField(blank=True, upload_to='students/projects/%Y/%m/%d/')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
                ('tag', models.CharField(max_length=150, blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Student Projects',
                'verbose_name': 'Student Project',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProjectSupervision',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('status', models.CharField(default='A', choices=[('A', 'Active'), ('D', 'Declined'), ('C', 'Completed'), ('R', 'Revoked')], max_length=1)),
                ('last_checked', models.DateTimeField(auto_now=True, null=True)),
                ('lecturer', models.ForeignKey(to='institutions.Lecturer', null=True)),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
            ],
        ),
    ]
