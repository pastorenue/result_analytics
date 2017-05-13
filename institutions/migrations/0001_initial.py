# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
            ],
            options={
                'ordering': ('faculty', 'name'),
                'verbose_name_plural': 'Departments',
                'verbose_name': 'Department',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=5, null=True)),
                ('name', models.CharField(max_length=250, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Faculties',
                'verbose_name': 'Faculty',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('location', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Institutions',
                'verbose_name': 'Institution',
            },
        ),
        migrations.CreateModel(
            name='InstitutionDetail',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, upload_to='institution/logo/%Y/%m/')),
                ('postal_code', models.CharField(blank=True, max_length=30, null=True)),
                ('full_address', models.TextField(blank=True, null=True)),
                ('institution', models.ForeignKey(null=True, to='institutions.Institution')),
            ],
            options={
                'ordering': ('institution',),
                'verbose_name_plural': 'Institution Complete Details',
                'verbose_name': 'Institution Complete Detail',
            },
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.PositiveIntegerField(blank=True, null=True, choices=[(1, 'Mr'), (2, 'Mrs'), (3, 'Miss'), (4, 'Dr'), (5, 'Prof'), (6, 'Mallam'), (7, 'Chief'), (8, 'Alhaji'), (9, 'Alhaja'), (10, 'J.P.')])),
                ('name', models.CharField(max_length=250, null=True)),
                ('specialty', models.CharField(blank=True, max_length=170, null=True)),
                ('department', models.ForeignKey(null=True, to='institutions.Department')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Lecturers',
                'verbose_name': 'Lecturer',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('reports_to', models.ForeignKey(null=True, blank=True, related_name='reports', to='institutions.Position')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Positions',
                'verbose_name': 'Position',
            },
        ),
        migrations.AddField(
            model_name='lecturer',
            name='position',
            field=models.ForeignKey(null=True, blank=True, to='institutions.Position'),
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(to='institutions.Faculty', null=True, related_name='department'),
        ),
    ]
