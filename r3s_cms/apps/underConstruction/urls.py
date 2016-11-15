from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
	url(r'.*$' , underconstruction_landingpage , name = 'underconstruction_landingpage') ,
)