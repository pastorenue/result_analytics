from django.shortcuts import render, get_object_or_404
from friendship.models import Friend, Follow, FriendshipRequest
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from students.models import Student
from notifications.signals import notify
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.db import transaction
from utils.url_dispatcher import get_url
try:
	import json
except:
	import simplejson as json

@login_required
def collaboration_index(request):
	context = {}
	try:
		context['friends'] = Friend.objects.friends(request.user)
		context['requests'] = Friend.objects.unread_requests(user=request.user)
		context['followers'] = Follow.objects.followers(request.user)
		context['follows'] = Follow.objects.following(request.user)
	except Exception as e:
		messages.error(request, e)
	return render(request, 'collaborations/collaboration_index.html', context)


@login_required
@transaction.atomic
def send_request(request):
	if request.method == "POST":
		other_user_id = request.POST.get('other_user_id')
		other_user = User.objects.get(pk=other_user_id)
		message = request.POST.get('message', '')
		if message == '':
			message = "%s needs your help and would like to collaborate with you" % (other_user.last_name)
		try:
			friend_request = Friend.objects.add_friend(request.user, other_user,                                
    			message=message)
			notify.send(request.user, recipient=other_user, 
				description=get_url(request,reverse('collaborate:collaboration_index')),
				verb="%s sent you a collaboration request." % (request.user.first_name))
			messages.success(request, "Your request has been sent")
		except Exception as e:
			messages.error(request, e)
	return HttpResponseRedirect(reverse('collaborate:collaboration_index'))


@login_required
@transaction.atomic
def accept_request(request, friend_request_id):
	friend_request = FriendshipRequest.objects.get(pk=friend_request_id)
	friend_request.accept()
	try:
		notify.send(request.user, recipient=friend_request.from_user, 
			description=get_url(request,reverse('collaborate:collaboration_index')),
			verb="%s has accepted your collaboration request." % (request.user.first_name))
		messages.success(request, "Friendship accepted")
	except Exception as e:
		messages.error(e)
	return HttpResponseRedirect(reverse('collaborate:collaboration_index'))


@login_required
@transaction.atomic
def cancel_friendship(request, other_user_id):
	other_user = get_object_or_404(User, pk=other_user_id)
	message = {"success": True}
	try:
		Friend.objects.remove_friend(request.user, other_user)
		notify.send(request.user, recipient=other_user, 
			description=get_url(request,reverse('collaborate:collaboration_index')),
			verb="%s has cancelled the existing collaborations between the both of you." % (request.user.first_name))
		messages.info(request, "You just destroyed your friend relationship with %s. \
					Feel free to leave us a comment on your reason for \
					quiting." % (Student.objects.get(user=other_user)))
	except Exception as e:
		messages.error(e)
	return HttpResponseRedirect(reverse('collaborate:collaboration_index'))

@login_required
@transaction.atomic
def reject_request(request, friend_request_id):
	friend_request = FriendshipRequest.objects.get(pk=friend_request_id)
	friend_request.reject()
	try:
		notify.send(request.user, recipient=friend_request.from_user, 
			description=get_url(request,reverse('collaborate:collaboration_index')),
			verb="%s rejected your collaboration request." % (request.user.first_name))
		messages.info(request, "Friendship rejected")
	except Exception as e:
		messages.error(e)
	message = {"success": True}
	return HttpResponseRedirect(reverse('collaborate:collaboration_index'))


@login_required
@transaction.atomic
def follow(request, to_user_id):
	try:
		to_user = User.objects.get(pk=to_user_id)
		from_user = request.user
		Follow.objects.add_follower(from_user, to_user)
		notify.send(request.user, recipient=to_user, 
			description=get_url(request,reverse('collaborate:collaboration_index')),
			verb="%s has started following you" % (request.user.first_name))
		messages.success(request, "You are currently following %s" % (to_user.last_name))
		return HttpResponseRedirect(reverse('collaborate:collaboration_index'))
	except Exception as e:
		messages.error(request, e)
		return HttpResponseRedirect(reverse('collaborate:collaboration_index'))

@login_required
def friend_zone(request):
	template_name = 'collaborations/all_collaborator.html'
	paginated_by = settings.PAGE_SIZE

	all_students = Student.objects.all().exclude(user=request.user)
	queryset = all_students
	paginator = Paginator(queryset, paginated_by)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	context = {'all_friends': queryset}
	return render(request, template_name, context)

@login_required
def mark_all_as_read(request):
	data = {}
	if request.is_ajax():
		request.user.notifications.mark_all_as_read()
		messages.success(request, "all notifications successfully marked as read")
		all_msg = []
		for msg in messages.get_messages(request):
			all_msg.append({
				'message':msg.message,
				'level': msg.level,
				'tags':msg.tags
				})
		data['messages'] = all_msg
		return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
	else:
		raise Http404