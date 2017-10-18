from django.shortcuts import render, get_object_or_404
from .models import Project
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from students.utils import user_is_student
from staff.models import Lecturer
import datetime

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
    	return Project.objects.filter(student=self.request.user.student).order_by('-last_modified')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_student))
    def dispatch(self, request, *args, **kwargs):
    	return super(ProjectListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
    	context = super(ProjectListView, self).get_context_data(**kwargs)
    	context['lecturers'] = Lecturer.objects.filter(institution=self.request.user.student.institution, 
    													department=self.request.user.student.department)
    	return context


class StaffProjectListView(ListView):
    model = Project
    template_name = 'projects/supervision_list.html'
    paginated_by = settings.PAGE_SIZE

    def get_queryset(self):
    	return Project.objects.filter(supervisor=self.request.user.lecturer).order_by('-last_modified')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.lecturer))
    def dispatch(self, request, *args, **kwargs):
    	return super(StaffProjectListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
    	context = super(StaffProjectListView, self).get_context_data(**kwargs)
    	queryset = self.get_queryset()
    	paginator = Paginator(queryset, self.paginated_by)
    	page = self.request.GET.get('page')

    	try:
    		queryset = paginator.page(page)
    	except PageNotAnInteger:
    		queryset = paginator.page(1)
    	except EmptyPage:
    		queryset = paginator.page(paginator.num_pages)
    	context['projects'] = queryset
    	context['year_list'] = [year for year in range(datetime.date.today().year, 1999+1, -1)]
    	return context

class ProjectDetailView(DetailView):
	model = Project
	template_name = 'projects/project_details.html'
	slug_url_kwarg = 'slug'
	pk_url_kwarg = 'pk'
	query_pk_and_slug = True
	context_object_name = 'project'

@login_required 
@transaction.atomic
def new_project(request):
	data = {}
	if request.method == 'POST':
		params = request.POST
		name = params.get('name', '')
		description = params.get('desc', '')
		category = params.get('category', '')
		file = request.FILES['file']
		tag = params.get('tag', '')
		lecturer_id = params.get('lecturer', '')
		supervisor = ''
		if lecturer_id:
			supervisor = get_object_or_404(Lecturer, pk=lecturer_id)
		project = Project(name=name, description=description, category=category, 
						file=file, tag=tag, supervisor=supervisor)
		project.student = request.user.student
		project.save()
		message = messages.success(request, "Your project: '%s', has successfully been created" % (project.name))
	return HttpResponseRedirect(reverse('my_projects'))


class LecturerSupervisionView(ListView):
    model = Project
    template_name = 'projects/supervision_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
    	return Project.objects.filter(supervisor=self.request.user.lecturer).order_by('-last_modified')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u:u.lecturer))
    def dispatch(self, request, *args, **kwargs):
    	return super(LecturerSupervisionView, self).dispatch(request, *args, **kwargs)

