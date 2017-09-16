from django import template
register = template.Library()

@register.filter
def get_dict_values(dict_collections, key, default=''):
	return dict_collections[key]
