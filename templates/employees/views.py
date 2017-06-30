from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from django.db.models.options import Options
from django.utils.text import camel_case_to_spaces as get_verbose_name
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.utils.cache import add_never_cache_headers
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView
from employees.models import Employee, Placement
from employees.forms import PlacementForm, ExitForm
from oxus.utils import is_ajax
from oxus.utils.excel import ExcelReport
from datetime import date

class EmployeeListView(ListView):
    model = Employee
    queryset = Employee.objects.get_active_employees()
    template_object_name = 'employee'
    template_name = 'employees/employee_list.html'
    paginate_by = settings.ITEMS_PER_PAGE
    allow_empty = True

def employee_profile(request, employee_id=None):
    employee = get_object_or_404(Employee, pk=employee_id) if employee_id else request.user.employee
    is_own_profile = (employee.user == request.user)
    template_name = 'employee_profile' if (is_own_profile or request.user.has_perm('can_manage_employees')) else 'employee_public_profile'
    return render(request, 'employees/%s.html' % template_name,
                            {'employee': employee, 'is_own_profile': is_own_profile})

def manage_employee_info(request, form_class, employee_id=None):
    template_name = '_inline_form.html' if is_ajax(request) else 'form.html'
    title = get_verbose_name(form_class.__name__[:-4])
    if employee_id:
        employee = get_object_or_404(Employee, pk=employee_id)
        form_kwargs = {'instance': employee}
    else:
        employee = None
        form_kwargs = {}
    if request.method == 'POST':
        form_kwargs.update({'data': request.POST, 'files': request.FILES})
        form = form_class(**form_kwargs)
        if form.is_valid():
            employee = form.save()
            if is_ajax(request):
                # We're probably calling this view from the profile page;
                # Render the appropriate partial template:
                name = form_class.__name__[:-4].lower()
                is_own_profile = (employee.user == request.user)
                response = TemplateResponse(request, 'employees/_%s.html' % name,
                                            {'employee': employee, 'edited': True, 'is_own_profile': is_own_profile})
                add_never_cache_headers(response)
                return response
            else:
                # Otherwise, redirect to employee profile:
                return redirect(employee)
    else:
        form = form_class(**form_kwargs)
    return TemplateResponse(request, 'employees/%s' % template_name, {'form': form, 'employee': employee, 'title': title})

def manage_additional_info(request, form_class, model, employee_id, id=None):
    template_name = '_inline_form.html' if is_ajax(request) else 'additional_info_form.html'
    title = get_verbose_name(form_class.__name__[:-4])
    instance = get_object_or_404(model, pk=id) if id else None
    edited = True if instance else False
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            if not id:
                instance.employee = employee
            instance.save()
            if is_ajax(request):
                template_name = 'employees/_%s.html' % model.__name__.lower()
                return TemplateResponse(request, template_name, {model.__name__.lower(): instance, 'employee': employee, 'edited': True})
            else:
                message = _(u'%(title)s has been %(action)s') % {'title': title, 'action': (_(u'updated') if edited else _(u'added'))}
                messages.success(request, message)
                return redirect(employee)
    else:
        form = form_class(instance=instance)
    return TemplateResponse(request, 'employees/%s' % template_name, {'form': form, 'instance': instance, 'employee': employee, 'title': title})

@ensure_csrf_cookie
def delete_additional_info(request, model_name, id):
    try:
        model = get_model('employees', model_name)
        instance = model.objects.get(pk=id)
    except (AttributeError, ObjectDoesNotExist):
        raise Http404(_(u'Requested %(name)s does not exist.') % {'name': model_name})
    employee = instance.employee
    opts = instance.__class__._meta
    if request.method == 'POST':
        instance.delete()
        if request.is_ajax():
            return HttpResponse(mimetype='text/plain', content='OK')
        else:
            messages.success(request, _(u'%(title)s "%(instance)s" has been deleted.') % {'title': opts.verbose_name, 'instance': unicode(instance)})
            return redirect(employee)
    else:
        return TemplateResponse(request, 'employees/delete_additional_info.html', {'instance': instance, 'employee': employee, 'opts': opts})

def password_change(request, template_name='registration/password_change_form.html'):
    try:
        employee = request.user.get_profile()
    except ObjectDoesNotExist:
        raise Http404(_(u'Employee "%(username)s" does not exist.') % {'username': request.user})
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u"Your password has been changed."))
            return redirect(employee)
    else:
        form = PasswordChangeForm(request.user)
    return TemplateResponse(request, template_name, {'form': form, 'employee': employee})

def export_employees(request):
    employees = ((e.user.last_name, e.user.first_name, e.staff_id_number, e.get_sex_display(), e.birth_date,
                  e.hire_date, e.grade_level.name, e.position.name, e.unit.name, e.location.name, unicode(e.bank or ''),
                  e.bank_account_number, unicode(e.pension_administrator or''), e.pfa_pin)
        for e in Employee.objects.order_by('user__last_name'))
    fields = ["last_name", "first_name", "staff_id_number", "sex", "birth_date", "hire_date", "grade_level", "position",
              "unit", "location", "bank", "bank_account_number", "pension_administrator", "pfa_pin"]
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=employees.xls"
    report = ExcelReport(employees, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response

def new_placement(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = PlacementForm(request.POST, employee=employee)
        if form.is_valid():
            placement = form.save(commit=False)
            if placement.position != employee.position or \
               placement.location != employee.location or \
               placement.unit != employee.unit:
                placement.employee = employee
                placement.save()
                employee.position = placement.position
                employee.unit = placement.unit
                employee.location = placement.location
                employee.save()
                messages.success(request, _(u"%(name)s's placement has been changed successfully.") % {'name': employee.full_name})
            return redirect('employees_employee_profile', employee_id=employee.id)
    else:
        form = PlacementForm(employee=employee)
    return TemplateResponse(request, 'employees/placement_form.html', {'form': form, 'employee': employee})

class PlacementListView(ListView):
    template_name='employees/placements.html'

    def get_queryset(self):
        self.employee = get_object_or_404(Employee, pk=self.kwargs['employee_id'])
        return self.employee.placements.all()

    def get_context_data(self, **kwargs):
        context = super(PlacementListView, self).get_context_data(**kwargs)
        context['employee'] = self.employee
        return context

## FIXME: This should definitely require some kind of permission!!
def terminate(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = ExitForm(request.POST)
        if form.is_valid():
            termination = form.save(commit=False)
            termination.employee = employee
            termination.user = request.user
            termination.save()
            if termination.exit_date <= date.today():
                employee.status = Employee.EX_EMPLOYEE
                employee.save()
            else:
                # TODO: Schedule task for exit date (change employee.status)
                #or add notice for employee status to be changed on the date
                pass
            messages.success(request, _(u"%(name)s's exit process has been started successfully.") % {'name': employee.full_name})
            return redirect('employees_employee_profile', employee_id=employee.id)
    else:
        form = ExitForm()
    return TemplateResponse(request, 'employees/exit_form.html', {'form': form, 'employee': employee})
