# -*- coding: utf-8 -*-
from r3s_cms.lib import render
from django.core.urlresolvers import reverse

def underconstruction(template = None , content_type = None , **kwargs):
	path = 'underConstruction'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)

@underconstruction(template = 'landing.html' , content_type = 'html')
def underconstruction_landingpage(request):
	return {}