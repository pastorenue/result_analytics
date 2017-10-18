from django.shortcuts import render
import datetime
from django.db.models import * 
from results.models import Result
from .models import Lecturer
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
#from chartit import DataPool, Chart
from django.core.urlresolvers import reverse
from analyzer.utils import ResultData
from courses.models import Course
from projects.models import Project
from django.contrib import messages
from django.forms.models import model_to_dict
from institutions.models import Department
from results.utils import import_result_from_csv
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import (user_is_staff, 
					staff_analytics_metrics, 
					import_quiz_from_csv,
					import_all_from_csv,
					import_assignment_from_csv)
try:
	import json
except:
	import simplejson as json

@user_passes_test(user_is_staff, login_url='/login/')
@login_required
def accounts(request):
	return render(request, 'staff/accounts.html', {})


class StaffListView(ListView):
	model = Lecturer
	template_name = 'staff/staff_list.html'
	paginated_by = settings.PAGE_SIZE

	def get_queryset(self):
		logged_user = self.request.user.lecturer
		queryset = Lecturer.objects.filter(institution=logged_user.institution)
		return queryset
	
	def get_context_data(self, **kwargs):
		context = super(StaffListView, self).get_context_data(**kwargs)
		queryset = self.get_queryset()

		paginator = Paginator(queryset, self.paginated_by)
		page = self.request.GET.get('page')

		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
			queryset = paginator.page(1)
		except EmptyPage:
			queryset = paginator.page(paginator.num_pages)
		context['lecturers'] = queryset
		return context

class StaffAnalyticsView(TemplateView):
	template_name = 'staff/_analysis.html'

	def get_context_data(self, **kwargs):
		context = super(StaffAnalyticsView, self).get_context_data(**kwargs)
		context['courses'] = Course.objects.filter(lecturers=self.request.user.lecturer)
		context['departments'] = get_lecturer_data(self.request)['dept']
		context['staff_metrics'] = staff_analytics_metrics(self.request.user)
		context['years'] = [i for i in range(datetime.date.today().year, 1998, -1 )]
		context['projects'] = Project.objects.filter(supervisor=self.request.user.lecturer).order_by('-last_modified').count()

		return context

	@method_decorator(login_required)
	@method_decorator(user_passes_test(user_is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(StaffAnalyticsView, self).dispatch(request, *args, **kwargs)


@user_passes_test(user_is_staff, login_url='/login/')
@login_required
def chart_data_json(request):
	data = None
	params = request.GET

	level = params.get('level', '')
	course_id = params.get('course', '')
	semester = params.get('semester', '')
	dept_id = params.get('dept', 'all')
	year = params.get('year', '')
	name = params.get('name', '')
	course = Course.objects.get(pk=course_id)
	if course:
		if name == 'course_data':
			dept=None
			results = None
			if dept_id != 'all':
				dept = Department.objects.get(pk=dept_id)
				results = Result.objects.filter(course__lecturers=request.user.lecturer, 
												course=course, 
												department=dept,
												date_created__year=year)
				data = ResultData.get_result_by_lecturer(results)
			else:
				results = Result.objects.filter(course__lecturers=request.user.lecturer, 
												course=course, date_created__year=year)
				data = ResultData.get_result_by_lecturer(results)
		elif name == 'course_average_by_dept':
			data = ResultData.dept_avg_score(request.user.lecturer, course, year=year)
	return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(user_is_staff, login_url='/login/')
@login_required
def other_uploads(request):
	data = {}
	if request.method == 'POST':
		params = request.POST
		upload_type = params.get('upload_type', '')
		try:
			response = 0
			csv_file = request.FILES["file"]
			if not csv_file.name.endswith('.csv'):
			   	messages.error(request,'File is not CSV type')
			   	return HttpResponseRedirect(reverse("results:result_import"))
		    # If the file is too large
			if csv_file.multiple_chunks():
			    messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			    return HttpResponseRedirect(reverse("results:result_import"))
		    # else continue
			if upload_type == 'assignment_score':
				response = import_assignment_from_csv(csv_file, request.user.lecturer)
			elif upload_type == 'quiz_score':
				response = import_quiz_from_csv(csv_file, request.user.lecturer)
			elif upload_type == 'exam_score':
				response = import_result_from_csv(csv_file, request.user.lecturer)
			else:
				response = import_all_from_csv(csv_file, request.user.lecturer)
			if response > 0:
				messages.success(request, "Your records were successfully imported.\r\n Total Records: %s" % (response))
			else:
				messages.info(request, "It appears you do not have any new records to import.\r\n Total Records: %s" % (response))
		except Exception as e:
			messages.error(request, e)
			return HttpResponseRedirect(reverse("results:result_import"))
	#return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponseRedirect(reverse("results:students_results")) 


def get_lecturer_data(req):
	results = Result.objects.filter(course__lecturers=req.user.lecturer)
	dept_list = []
	for result in results:
		if result.student.department not in dept_list:
			dept_list.append(result.student.department)
	return {'dept':dept_list}


@login_required
@user_passes_test(lambda u: u.lecturer.is_admin)
def create_staff(request):
    if request.method == "POST":
        form = CustomStaffCreationForm(request.POST)
        if form.is_valid():
            try:
                staff = form.save(commit=False)
                staff.institution = request.user.lecturer.institution
                staff.save()
                messages.success(request, "%s's record has been successfully created." % (staff))
                return HttpResponseRedirect(reverse('staff-list'))
            except Exception as e:
                messages.error(request, e)
    else:
        form = CustomStaffCreationForm()
    return render(request, 'staff/new_staff.html', {'form': list(form)})


@login_required
def edit_profile(request):
    context ={}
    lecturer = Lecturer.objects.get(user=request.user)
    template_name = 'staff/_edit_profile.html'
    if request.method == 'POST':
        form = LecturerCreationForm(request.POST, request.FILES, instance=lecturer)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Your profile was successfully updated")
                return HttpResponseRedirect(reverse('staff_account'))
            except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('edit-profile'))
    else:
        form = LecturerCreationForm(instance=lecturer)
        context = {
            'form': form,
            'lecturer': lecturer
        }
    return render(request, template_name, context)

