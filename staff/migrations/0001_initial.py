# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, null=True, choices=[('Mr.', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr.', 'Dr'), ('Prof', 'Prof'), ('Mallam', 'Mallam')], max_length=5)),
                ('first_name', models.CharField(null=True, max_length=50)),
                ('last_name', models.CharField(null=True, max_length=50)),
                ('gender', models.CharField(null=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('marital_status', models.CharField(blank=True, null=True, choices=[(1, 'Single'), (2, 'Married'), (3, 'Widowed'), (4, 'Divorced')], max_length=1)),
                ('email', models.EmailField(null=True, max_length=254)),
                ('staff_id', models.CharField(blank=True, max_length=50)),
                ('specialty', models.CharField(blank=True, null=True, max_length=170)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('department', models.ForeignKey(to='institutions.Department', null=True)),
                ('institution', models.ForeignKey(to='institutions.Institution', null=True)),
            ],
            options={
                'ordering': ('first_name',),
                'verbose_name_plural': 'Lecturers',
                'verbose_name': 'Lecturer',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('reports_to', models.ForeignKey(to='staff.Position', null=True, related_name='reports', blank=True)),
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
            field=models.ForeignKey(to='staff.Position', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='lecturer'),
        ),
    ]
