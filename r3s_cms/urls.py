from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from r3s_cms.apps.system.views import system_login

urlpatterns = [
#	url(r'^auth' , include('r3s_cms.apps.systemAuth.urls')) ,
#	url(r'^imagery' , include('r3s_cms.apps.imagery.public_urls')) ,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [
#	url(r'^/' , include('r3s_cms.apps.content.urls')) ,
#	url(r'^' , include('r3s_cms.apps.underConstruction.urls')) ,
	url(r'^$' , system_login , name = 'system_login') ,
	url(r'^system' , include('r3s_cms.apps.system.urls')) ,
]
