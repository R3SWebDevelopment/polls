# -*- coding: utf-8 -*-
from r3s_cms.lib import render
from django.core.urlresolvers import reverse

def content(template = None , content_type = None , **kwargs):
	path = 'content'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)

@content(template = 'landing.html' , content_type = 'html')
def content_landing(request):
	return {
		'redirect' : True ,
		'url' : reverse('system_dashboard') ,
	}