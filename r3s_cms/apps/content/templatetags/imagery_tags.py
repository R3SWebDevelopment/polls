from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()


@register.assignment_tag(takes_context=True)
def cover_images(context):
	return []