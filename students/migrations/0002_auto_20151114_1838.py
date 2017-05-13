# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address1', models.TextField(null=True)),
                ('address2', models.TextField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
            ],
            options={
                'verbose_name': 'Phone Number',
                'verbose_name_plural': 'Phone Numbers',
                'ordering': ('number',),
            },
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='students',
        ),
        migrations.RemoveField(
            model_name='student',
            name='email',
        ),
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.ForeignKey(null=True, to='students.Address'),
        ),
        migrations.AlterField(
            model_name='student',
            name='user_status',
            field=models.CharField(null=True, max_length=30, choices=[(1, 'Barred'), (0, 'Active'), (2, 'Inactive')], blank=True),
        ),
        migrations.AddField(
            model_name='address',
            name='number',
            field=models.ForeignKey(null=True, to='students.PhoneNumber', max_length=15),
        ),
    ]
