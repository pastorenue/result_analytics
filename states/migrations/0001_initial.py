# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Countries',
                'verbose_name': 'Country',
            },
        ),
        migrations.CreateModel(
            name='LGA',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ('state', 'name'),
                'verbose_name_plural': 'Nigerian Local Government Areas',
                'verbose_name': 'Nigerian Local Government Area',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Nigerian States',
                'verbose_name': 'Nigerian State',
            },
        ),
        migrations.AddField(
            model_name='lga',
            name='state',
            field=models.ForeignKey(related_name='local_govt_areas', to='states.State'),
        ),
    ]
