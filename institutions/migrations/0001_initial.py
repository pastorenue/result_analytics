# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcadamicYear',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('year_starting', models.DateField()),
                ('year_ending', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AdminStaff',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(null=True, max_length=3)),
                ('id_number', models.IntegerField(null=True, blank=True)),
                ('name', models.CharField(null=True, max_length=200)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Departments',
                'verbose_name': 'Department',
            },
        ),
        migrations.CreateModel(
            name='DepartmentalCode',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(null=True, max_length=50)),
                ('code', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Departmental Codes',
                'verbose_name': 'Departmental Code',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(null=True, max_length=5)),
                ('name', models.CharField(null=True, max_length=250)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(null=True, max_length=250)),
                ('location', models.CharField(blank=True, null=True, max_length=150)),
                ('logo', models.ImageField(blank=True, upload_to='institution/logo/%Y/%m/')),
                ('postal_code', models.CharField(blank=True, null=True, max_length=30)),
                ('full_address', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Institutions',
                'verbose_name': 'Institution',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(to='institutions.Faculty', null=True, related_name='department'),
        ),
        migrations.AddField(
            model_name='adminstaff',
            name='institution',
            field=models.OneToOneField(to='institutions.Institution'),
        ),
        migrations.AddField(
            model_name='adminstaff',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
