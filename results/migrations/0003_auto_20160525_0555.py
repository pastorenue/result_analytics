# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20160525_0555'),
        ('results', '0002_auto_20151126_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='CGPA',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('cgpa', models.DecimalField(decimal_places=2, max_digits=3)),
                ('semester', models.PositiveIntegerField()),
                ('session', models.CharField(max_length=15)),
                ('level', models.PositiveIntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('student', models.ForeignKey(to='students.Student')),
            ],
            options={
                'verbose_name_plural': 'CGPAs',
                'verbose_name': 'CGPA',
                'ordering': ('date_created',),
            },
        ),
        migrations.AddField(
            model_name='result',
            name='date_modified',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='date_created',
            field=models.DateField(null=True, auto_now_add=True),
        ),
    ]
