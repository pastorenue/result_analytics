from django import template
register = template.Library()

@register.filter
def get_dict_values(dict_collections, key, default=''):
	return dict_collections[key]

@register.inclusion_tag('_pagination.html')
def render_paginator(object_list):
	return {'object_list': object_list}
