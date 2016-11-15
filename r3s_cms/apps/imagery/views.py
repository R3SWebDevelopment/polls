# -*- coding: utf-8 -*-
from r3s_cms.lib import render
from models import Album

def public_imagery(template = None , content_type = None , **kwargs):
	path = 'imagery/public'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)

@public_imagery(template = 'view.html' , content_type = 'html')
def public_album_view(request , album_id = None):
	error = True
	exception = None
	album = None
	if album_id:
		album = Album.objects.filter(id = album_id).first()
		if album:
			error = False
		else:
			exception = Exception('Album Image not Found')
	else:
		exception = Exception('Album ID Not Provided')
	return {
		'error' : error ,
		'exception' : exception ,
		'album' : album ,
	}
