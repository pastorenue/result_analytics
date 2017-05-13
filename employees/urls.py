from django.conf.urls import patterns, url
from careers.forms import CertificationForm
from employees.forms import *
from employees.models import Employee
from employees.views import EmployeeListView, PlacementListView
from leave.views import LeaveListView
from loan.views import LoanListView

urlpatterns = patterns('employees.views',
    url(r'^me/$', 'employee_profile', name='employees_my_profile'),
    url(r'^change-password/$', 'password_change', name='employees_change_password'),
    url(r'^$', EmployeeListView.as_view(), name='employees_list'),
    url(r'^add/$', 'manage_employee_info',
        {'form_class': EmployeeCreationForm}, name='employees_add_employee'),
    url(r'^(?P<employee_id>\d+)/$', 'employee_profile', name='employees_employee_profile'),
    url(r'^(?P<employee_id>\d+)/basicprofile/$', 'manage_employee_info',
        {'form_class': BasicProfileForm}, name='employees_basicprofile_edit'),
    url(r'^(?P<employee_id>\d+)/companyinfo/$', 'manage_employee_info',
        {'form_class': CompanyInformationForm}, name='employees_companyinfo_edit'),
    url(r'^(?P<employee_id>\d+)/personalinfo/$', 'manage_employee_info',
        {'form_class': PersonalInformationForm}, name='employees_personalinfo_edit'),
    url(r'^excel/$', 'export_employees', name='employees_export_employees'),
    url(r'^(?P<employee_id>\d+)/move/$', 'new_placement', name='employees_move_employee'),
    url(r'^(?P<employee_id>\d+)/placements/$', PlacementListView.as_view(), name='employees_employee_placements'),
    url(r'^(?P<employee_id>\d+)/exit/$', 'terminate', name='employees_exit'),
)

# Add URLs for additional info:
for form_class in (CertificationForm, NextOfKinForm, DependentForm, EducationForm, ExperienceForm, DocumentForm, LifeInsuranceForm, IncidenceForm):
    model = form_class._meta.model
    model_name = model._meta.model_name
    urlpatterns += patterns('employees.views',
        url(r'^(?P<employee_id>\d+)/%s/add/$' % model_name,
            'manage_additional_info',
            {'form_class': form_class, 'model': model},
            name='employees_%s_add' % model_name),
        url(r'^(?P<employee_id>\d+)/%s/(?P<id>\w+)/$' % model_name,
            'manage_additional_info',
            {'form_class': form_class, 'model': model},
            name='employees_%s_edit' % model_name),
        url(r'^%s/(?P<id>\d+)/delete/$' % model_name,
            'delete_additional_info',
            {'model_name': model_name},
            name='employees_%s_delete' % model_name)
        )

urlpatterns += patterns('careers.views',
    url(r'^(?P<employee_id>\d+)/skills/$', 'manage_employee_skills', name='employees_skills_manage')
)

#######################
## Self-Service URLs ##
#######################

urlpatterns += patterns('appraisals.views',
    url(r'^(?P<employee_id>\w+)/appraisals/schedule/$', 'schedule_appraisal', name='appraisals_schedule_appraisal'),
    url(r'^(?P<employee_id>\w+)/appraisals/complete/$', 'complete_appraisal', name='appraisals_complete_appraisal'),
    url(r'^(?P<employee_id>\d+)/appraisals/(?P<appraisal_id>\d+)/pdf/$', 'view_appraisal', {'as_pdf': True}, name='appraisals_download_as_pdf'),
    url(r'^(?P<employee_id>\d+)/appraisals/(?P<appraisal_id>\d+)/$', 'view_appraisal', name='appraisals_view_appraisal'),
    url(r'^(?P<employee_id>\d+)/appraisals/$', 'history', name='employees_appraisal_history'),
)

urlpatterns += patterns('extendmodels.views',
    url(r'^fields/(?P<type>\w+)/(?P<field_id>\d+)/delete/$', 'delete', name='employees_delete_additional_field'),
    url(r'^fields/(?P<type>\w+)/(?P<field_id>\d+)/edit/$', 'manage', {'app_label': 'employees', 'model': 'employee'}, name='employees_edit_additional_field'),
    url(r'^fields/(?P<type>\w+)/add/$', 'manage', {'app_label': 'employees', 'model': 'employee'}, name='employees_add_additional_field'),
    url(r'^fields/$', 'list', {'app_label': 'employees', 'model': 'employee'}, name='employees_list_additional_fields'),
    url(r'^(?P<object_id>\d+)/additionalinfo/$', 'manage_field_data', {'model': Employee}, name='employees_additional_fields_edit_data'),
)

urlpatterns += patterns('promotion.views',
    url(r'^(?P<employee_id>\d+)/promotions/$', 'history', name='employees_promotion_history'),
)

urlpatterns += patterns('payprocess.views',
    url(r'^(?P<employee_id>\d+)/info/$', 'payinfo', name='employees_payinfo'),
    url(r'^(?P<employee_id>\d+)/payslips/$', 'employee_payslips', {'template_name': 'selfservice/payslip_list.html'}, name='employees_my_payslips'),
    url(r'^(?P<employee_id>\d+)/payslips/(?P<id>\d+)/$', 'employee_pay_detail', {'template_name': 'selfservice/payslip.html'}, name='employees_payslip_details'),
    url(r'^(?P<employee_id>\d+)/payslips/(?P<id>\d+)/pdf/$', 'employee_payslip_pdf', name='employees_payslip_pdf'),
    url(r'^(?P<employee_id>\d+)/pension-contributions/$', 'pension_history', {'template_name':'selfservice/pension_history.html'}, name='employees_pension_contributions'),
    url(r'^(?P<employee_id>\d+)/formula/(?P<formula_id>\d+)/override/$', 'override_formula', name='employees_override_formula'),
)

urlpatterns += patterns('loan.views',
    url(r'^(?P<employee_id>\d+)/loans/apply/$', 'new_loan', {'template_name':'employees/loans/apply.html'}, name='employees_new_loan'),
    url(r'^(?P<employee_id>\d+)/loans/$', LoanListView.as_view(template_name='employees/loans/all.html'), name='employees_employee_loans'),
)

urlpatterns += patterns('leave.views',
    url(r'^(?P<employee_id>\d+)/leave/apply/$', 'new_leave', {'template_name':'employees/leave/apply.html'}, name='employees_new_leave'),
    url(r'^(?P<employee_id>\w+)/leave/$', LeaveListView.as_view(template_name='employees/leave/all.html'), name='employees_leave_history'),
)

urlpatterns += patterns('claim.views',
    url(r'^claims/apply/$', 'new_claim', {'template_name':'claim/apply.html'}, name='employees_new_claim'),
    url(r'^claims/(?P<employee_id>\d+)$', 'my_claims', name='employees_employee_claims'),
)