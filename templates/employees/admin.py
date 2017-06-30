from django.contrib import admin
from employees.models import *

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1

class DependentInline(admin.TabularInline):
    model = Dependent
    extra = 1

class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 1

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('staff_id_number', 'full_name', 'position', 'unit', 'location', 'phone')
    search_fields = ['staff_id_number', 'user__first_name', 'user__last_name']
    fieldsets = [
        ('Personal Information', {
            'fields': ('staff_id_number', 'photo', 'title', 'middle_name', 'marital_status', 'maiden_name', 'mothers_maiden_name',
                       'sex', 'birth_date', 'blood_group', 'genotype', 'phone', 'address',)
        }),
        ('Company Information', {
            'fields': ('employee_type', 'grade_level', 'basic', 'pay_template', 'position', 'unit', 'location', 'status', 'hire_date',
                       'confirmation_date', 'termination_date',)
        }),
        ('Salaries & Pension', {
            'fields': ('bank', 'bank_account_number', 'skip_nhf', 'skip_nhis', 'skip_nsitf', 'skip_pension', 'pension_administrator', 'pfa_pin', 'tax_id', 'state_of_residence',)
        }),
        ('Others', {
            'fields': ('religion', 'national_id_number', 'passport_number', 'permanent_address', 'state_of_origin', 'lga', 'country',)
        })
    ]
    readonly_fields = ('grade_level', 'confirmation_date',
                       'termination_date',)
    inlines = [EducationInline, ExperienceInline, DependentInline, NextOfKinInline]

class PensionAdministratorAdmin(admin.ModelAdmin):
    list_display = ('name', 'custodian')

class IncidenceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class IncidenceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'incidence_type', 'incidence_date', 'record_date', 'remarks')

admin.site.register(Bank)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeType)
admin.site.register(PensionAdministrator, PensionAdministratorAdmin)
admin.site.register(PensionCustodian)
admin.site.register(InsuranceCompany)
admin.site.register(Termination)
admin.site.register(IncidenceType, IncidenceTypeAdmin)
admin.site.register(Incidence, IncidenceAdmin)
