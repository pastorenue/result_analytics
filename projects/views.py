from django.shortcuts import render, get_object_or_404
from .models import Project
from django.views.generic import ListView, DetailView
from .forms import *
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
		file = request.FILES['file'] or None
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


@login_required
@user_passes_test(user_is_student)
@transaction.atomic
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {}
    template_name = 'projects/edit_project.html'

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Your project was successfully updated")
            return HttpResponseRedirect(reverse('my_projects'))
    else:
        form = ProjectForm(instance=project)
        form.fields['supervisor'].queryset = Lecturer.objects.filter(institution=request.user.student.institution)
        context['form'] = form
    context['project'] = project
    return render(request, template_name, context)


class LecturerSupervisionView(ListView):
    model = Project
    template_name = 'projects/supervision_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = Project.objects.filter(supervisor=self.request.user.lecturer).order_by('-last_modified')
        params = self.request.GET
        year = params.get('year', 'all')
        level = params.get('level', 'all')
        import pdb
        pdb.set_trace()

        if level != 'all':
            queryset = queryset.filter(student__level=level)
        if year != 'all':
            queryset = queryset.filter(date_created__year=year)
        return queryset

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: hasattr(u, 'lecturer'), login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
    	return super(LecturerSupervisionView, self).dispatch(request, *args, **kwargs)

