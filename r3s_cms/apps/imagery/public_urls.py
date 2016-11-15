from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
	url(r'/album/(?P<album_id>\w+)/view/$' , public_album_view , name = 'public_album_view') ,
)