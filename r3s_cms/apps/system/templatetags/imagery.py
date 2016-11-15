from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()


@register.assignment_tag(takes_context=True)
def photo_albums_count(context , currentSection = None):
	return 0
	
@register.assignment_tag(takes_context=True)
def public_cover_images(context):
	from r3s_cms.apps.imagery.models import Album , AlbumImage
	cover = Album.objects.exclude(active = False).exclude(published = False).exclude(cover = False).first()
	if cover:
		images = cover.getPublishedImages
	else:
		images = AlbumImage.objects.none()
	return images
	
@register.assignment_tag(takes_context=True)
def get_public_albums(context):
	from r3s_cms.apps.imagery.models import Album
	albums = Album.objects.all().exclude(active = False).exclude(published = False).exclude(cover = True)
	return albums