from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
	url(r'/list/$' , system_dashboard , name = 'system_dashboard') ,
	url(r'/imagery/$' , system_imagery , name = 'system_imagery') ,
)