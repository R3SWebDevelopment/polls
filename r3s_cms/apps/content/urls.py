from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
	url(r'$' , content_landing , name = 'content_landing') ,
)