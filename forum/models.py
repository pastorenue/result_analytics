from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name = _(u'Forum Category')
		verbose_name_plural = _(u'Forum Categories')
		ordering = ('name',)

	def __str__(self):
		return self.name

	def last_post(self):
		if self.post_set.count():
			return self.post_set.order_by("created")[0]


class Post(models.Model):
	POST_CHOICES = (
		('Q', 'Question'),
		('I', 'Idea')
	)
	user = models.ForeignKey(User)
	title = models.CharField(max_length=50)
	post_type = models.CharField(max_length=1, choices=POST_CHOICES)
	category = models.ForeignKey(Category)
	question_or_idea = models.TextField(_(u'Your question or Idea to Share'), 
						help_text="Make your post as clear as possible for quick feedback")
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _(u'Post')
		verbose_name_plural = _(u'Posts')

	def __str__(self):
		return self.title


class Response(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	comment = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-date_created',)

	def __str__(self):
		return "%s - %s" % (self.user.last_name, self.comment[:20])


class Reply(models.Model):
	user = models.ForeignKey(User)
	response = models.ForeignKey(Response)
	comment = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.comment[:20]

class ProfaneWord(models.Model):
    word = models.CharField(max_length=60)

    def __str__(self):
        return self.word
