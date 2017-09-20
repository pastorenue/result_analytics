from django.contrib.sites.shortcuts import get_current_site

def get_url(request, url):
	#Returns the absolute url of a particualar path
	
	current_site = get_current_site(request).domain
	full_url_path = ''.join(['http://', current_site, url])
	return full_url_path