from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):

	class Meta:
		model = Post
		list_display = ('title', 'category', 'post_type')

class CategoryAdmin(admin.ModelAdmin):

	class Meta:
		model = Category
		list_display = ('name')

class ProfaneWordAdmin(admin.ModelAdmin):

	class Meta:
		model = ProfaneWord
		list_display = ('word',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ProfaneWord, ProfaneWordAdmin)