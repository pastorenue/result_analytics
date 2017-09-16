from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse 
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .models import AssignmentScore, Assignment
from students.utils import user_is_student
from django.http import HttpResponseRedirect 
from django.contrib import messages
from courses.models import Course
from .forms import AssignmentForm, AssignmentSubmitForm
try:
	import json
except:
	import simplejson as json

def user_is_staff(user):
	return user.is_staff

class AssignmentScoreListView(ListView):
	model = AssignmentScore
	template_name = "assignments/list_assignments.html"
	context_object_name = "assignments"
	ordering = ['date_created']

	@method_decorator(login_required)
	@method_decorator(user_passes_test(user_is_student))
	def dispatch(self, request, *args, **kwargs):
		return super(AssignmentScoreListView, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return AssignmentScore.objects.filter(student=self.request.user.student).order_by('-date_created')


class AssignmentView(ListView):
	model = Assignment
	template_name = "assignments/staff_assignments.html"
	context_object_name = "assignments"

	@method_decorator(login_required)
	@method_decorator(user_passes_test(user_is_staff))
	def dispatch(self, request, *args, **kwargs):
		return super(AssignmentView, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		queryset = Assignment.objects.filter(lecturer=self.request.user.lecturer)
		course = self.request.GET.get('course', 'all')
		level = self.request.GET.get('level', 'all')
		category = self.request.GET.get('category', 'all')

		if course != 'all':
			queryset = queryset.filter(course__name__icontains=course)
		if level != 'all':
			queryset = queryset.filter(level=level)
		if category != 'all':
			queryset = queryset.filter(category__icontains=category)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(AssignmentView, self).get_context_data(**kwargs)
		context['courses'] = Course.objects.filter(lecturer=self.request.user.lecturer)
		return context


@login_required
def assignment_detail(request, assignment_code):
	assignment = get_object_or_404(Assignment, assignment_code=assignment_code)

	data = {}
	data['assignment'] = assignment
	return JsonResponse(json.dumps(data), content_type="application/json")


@user_passes_test(user_is_staff)
@login_required
def create_assignment(request):
	if request.method == "POST":
		form = AssignmentForm(request.POST, request.FILES, request=request)
		if form.is_valid:
			form.save()
			messages.success(request, "Assignment has been created successfully")
			return HttpResponseRedirect(reverse('staff_account'))
	else:
		form = AssignmentForm()
	return render(request, 'assignments/create_assignment.html', {'form':form})


@user_passes_test(user_is_student)
@login_required
def submit_assignment(request, assignment_code):
	assignment = get_object_or_404(Assignment, assignment_code=assignment_code)

	if request.method == "POST":
		form = AssignmentSubmitForm(request.POST, request.FILES)
		if form.is_valid:
			form = form.save(commit=False)
			form.assignment = assignment
			form.student = request.user.student
			form.save()

			ass_score = AssignmentScore.objects.filter(assignment=assignment, student=request.user.student)[0]
			ass_score.status = 'S'
			ass_score.save()
			messages.success(request, "Your assignment has been submitted successfully.")
			return HttpResponseRedirect(reverse('assignment:all_assignments'))
	else:
		form = AssignmentSubmitForm()
	return render(request, 'assignments/submit_assignments.html', {'form':form, 'assignment': assignment})