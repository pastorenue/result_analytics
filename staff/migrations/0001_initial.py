# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_auto_20170919_1036'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=5, null=True, blank=True, choices=[('Mr.', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr.', 'Dr'), ('Prof', 'Prof'), ('Mallam', 'Mallam')])),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('gender', models.CharField(max_length=1, null=True, choices=[('M', 'Male'), ('F', 'Female')])),
                ('marital_status', models.CharField(max_length=1, null=True, blank=True, choices=[(1, 'Single'), (2, 'Married'), (3, 'Widowed'), (4, 'Divorced')])),
                ('email', models.EmailField(max_length=254, null=True)),
                ('staff_id', models.CharField(max_length=50, blank=True)),
                ('specialty', models.CharField(max_length=170, null=True, blank=True)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('department', models.ForeignKey(to='institutions.Department', null=True)),
                ('institution', models.ForeignKey(to='institutions.Institution', null=True)),
            ],
            options={
                'verbose_name': 'Lecturer',
                'verbose_name_plural': 'Lecturers',
                'ordering': ('first_name',),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('reports_to', models.ForeignKey(null=True, to='staff.Position', blank=True, related_name='reports')),
            ],
            options={
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='lecturer',
            name='position',
            field=models.ForeignKey(null=True, to='staff.Position', blank=True),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='lecturer'),
        ),
    ]
