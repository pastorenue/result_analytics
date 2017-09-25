from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Response, Reply
from .forms import PostForm, CategoryForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.contrib import messages
from students.models import Student
from django.db.models import Q


def user_is_student(user):
	try:
		return Student.objects.filter(user=user).exists()
	except TypeError as e:
		return redirect('/login/')
# Create your views here.

@user_passes_test(user_is_student, login_url='/login/')
@login_required
def forum_index(request):
	template_name = 'forum/forum.html'
	queryset = Q()

	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid:
			form = form.save(commit=False)
			form.user = request.user
			form.save()
			messages.success(request, "You have successfully started the discussion-'%s'" % (form.title))
			return HttpResponseRedirect(reverse('post', args=(form.id,)))
	else:	
		search = request.GET.get('search_query', 'invalid_search')
		category = request.GET.get('category')
		comment_qs = Q(comment__icontains=search)
		category_qs = Q(post__category__name__icontains=search)
		post_qs = Q(post__question_or_idea__icontains=search)
		title_qs = Q(post__title__icontains=search)
		queryset = Response.objects.filter(post_qs|title_qs) or Post.objects.filter(Q(question_or_idea__icontains=search) | Q(title__icontains=search))

		if category != 'All Categories' and category is not None:
			queryset = Post.objects.filter(category__name__icontains=category)
		else:
			queryset = Post.objects.all()
		form = PostForm()
	return render(request, template_name, {'form': list(form), 'queryset':queryset})



@user_passes_test(user_is_student, login_url='/login/')
@login_required
def post(request, post_id):
	post = get_object_or_404(Post, pk=post_id) 

	return render(request, 'forum/post.html', {'post': post})


@user_passes_test(user_is_student, login_url='/login/')
@login_required
def new_response(request, post_id):
	if request.method == "POST":
		post = get_object_or_404(Post, pk=post_id)
		comment = request.POST.get('comment')
		try:
			if comment:
				response = Response.objects.create(user=request.user, post=post, comment=comment)
				messages.success(request, "Your response has been saved")
		except:
			messages.error(request, "Could not commit your response")
	return HttpResponseRedirect(reverse('post', args=(post.id,)))


def new_category(request):
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid:
			form.save()
		return render(request, 'forum/new_category.html', {'form': form})


@user_passes_test(user_is_student, login_url='/login/')
@login_required
def new_reply(request, post_id, response_id):
	if request.method == "POST":
		post = get_object_or_404(Post, pk=post_id)
		response = get_object_or_404(Response, pk=response_id, post=post)
		comment = request.POST.get('reply')
		try:
			reply = Reply.objects.create(user=request.user, comment=comment, response=response)
			messages.success(request, "Your reply has been saved")
		except:
			messages.error(request, "Could not commit your reply")
	return HttpResponseRedirect(reverse('post', args=(post.id,)))
