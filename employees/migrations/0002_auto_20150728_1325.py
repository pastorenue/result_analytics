# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0001_initial'),
        ('salary', '0001_initial'),
        ('states', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='placement',
            name='location',
            field=models.ForeignKey(related_name='placements', to='organization.Location'),
        ),
        migrations.AddField(
            model_name='placement',
            name='position',
            field=models.ForeignKey(related_name='placements', to='organization.Position'),
        ),
        migrations.AddField(
            model_name='placement',
            name='unit',
            field=models.ForeignKey(related_name='placements', to='organization.Unit'),
        ),
        migrations.AddField(
            model_name='pensioncustodian',
            name='bank',
            field=models.ForeignKey(blank=True, to='employees.Bank', null=True),
        ),
        migrations.AddField(
            model_name='pensionadministrator',
            name='custodian',
            field=models.ForeignKey(blank=True, to='employees.PensionCustodian', null=True),
        ),
        migrations.AddField(
            model_name='nextofkin',
            name='employee',
            field=models.ForeignKey(related_name='next_of_kin', editable=False, to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='lifeinsurance',
            name='employee',
            field=models.ForeignKey(related_name='insurance_policies', to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='lifeinsurance',
            name='insurer',
            field=models.ForeignKey(related_name='policies', to='employees.InsuranceCompany'),
        ),
        migrations.AddField(
            model_name='incidence',
            name='employee',
            field=models.ForeignKey(related_name='employee_incidences', to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='incidence',
            name='incidence_type',
            field=models.ForeignKey(to='employees.IncidenceType'),
        ),
        migrations.AddField(
            model_name='experience',
            name='employee',
            field=models.ForeignKey(related_name='experience', editable=False, to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='employee',
            name='bank',
            field=models.ForeignKey(blank=True, to='employees.Bank', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='country',
            field=models.ForeignKey(related_name='country_of_residence', blank=True, to='states.Country', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_type',
            field=models.ForeignKey(blank=True, to='employees.EmployeeType', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='grade_level',
            field=models.ForeignKey(related_name='employees', to='organization.GradeLevel'),
        ),
        migrations.AddField(
            model_name='employee',
            name='lga',
            field=models.ForeignKey(related_name='employees', verbose_name='LGA', blank=True, to='states.LGA', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='location',
            field=models.ForeignKey(related_name='employees', to='organization.Location'),
        ),
        migrations.AddField(
            model_name='employee',
            name='pay_template',
            field=models.ForeignKey(related_name='employees', to='salary.PayTemplate'),
        ),
        migrations.AddField(
            model_name='employee',
            name='pension_administrator',
            field=models.ForeignKey(blank=True, to='employees.PensionAdministrator', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(related_name='employees', to='organization.Position', help_text="This employee's job title"),
        ),
        migrations.AddField(
            model_name='employee',
            name='state_of_origin',
            field=models.ForeignKey(related_name='employees_origin', blank=True, to='states.State', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='state_of_residence',
            field=models.ForeignKey(related_name='employees_residence', to='states.State', help_text='Your income tax will be remitted to this state.'),
        ),
        migrations.AddField(
            model_name='employee',
            name='unit',
            field=models.ForeignKey(related_name='employees', to='organization.Unit', help_text='The department or division this employee is being assigned to'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(related_name='employee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='education',
            name='employee',
            field=models.ForeignKey(related_name='institutions', editable=False, to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='document',
            name='ctype',
            field=models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='employee',
            field=models.ForeignKey(related_name='documents', editable=False, to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='dependent',
            name='employee',
            field=models.ForeignKey(related_name='dependents', editable=False, to='employees.Employee'),
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together=set([('pension_administrator', 'pfa_pin'), ('bank', 'bank_account_number')]),
        ),
    ]
