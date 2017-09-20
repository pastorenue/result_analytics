from django.contrib.sites.shortcuts import get_current_site

def get_url(request, url, protocol='https://'):
	current_site = get_current_site(request).domain
	full_url_path = ''.join([protocol, current_site, url])
	return full_url_path