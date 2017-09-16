from django import forms
from .models import Category, Post, Response, Reply

class CategoryForm(forms.ModelForm):

	class Meta:
		model = Category
		fields = ('name',)


class PostForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs = {'class': 'form-control', 'placeholder':'Descriptive Title'}
		self.fields['post_type'].widget.attrs = {'class': 'form-control'}
		self.fields['category'].widget.attrs = {'class': 'form-control'}
		self.fields['question_or_idea'].widget.attrs = {'class': 'form-control', 
														'rows':'4', 'placehoder':'Enter your question or idea here'}

	class Meta:
		model = Post
		exclude = ('user', 'created')

	def clean_body(self):
		body = self.cleaned_data["body"]

		if FILTER_PROFANE_WORDS:
		    profane_words = ProfaneWord.objects.all() 
		    bad_words = [w for w in profane_words if w.word in body.lower()]

		    if bad_words:
		        raise forms.ValidationError("Bad words like '%s' are not allowed in posts." % (reduce(lambda x,y: "%s,%s" % (x,y),bad_words)))

		return body


class ResponseForm(forms.ModelForm):

	class Meta:
		model = Response
		exclude = ('user', 'date_created')


class ReplyForm(forms.ModelForm):

	class Meta:
		model = Reply
		exclude = ('user', 'date_created')
