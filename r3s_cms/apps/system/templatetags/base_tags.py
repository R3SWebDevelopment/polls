from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_siteurl(context):
	siteurl = ''
	request = context['request'] or None
	if request:
		domain = request.get_host() or None
		if request.is_secure():
			scheme = 'https://'
		else:
			scheme = 'http://'			
		if domain and scheme:
			siteurl = "%s%s" % (scheme , domain)
	return siteurl

@register.assignment_tag(takes_context=True)
def get_column(context , data = None , column = None):
	if column in data.keys():
		column_data = data.get(column) or {}
	else:
		column_data = {}
	return column_data
	
@register.filter()
def currency(value):
	import unicodedata
	if value:
		if value == 0.00:
			value = u'0.00'
		else:
			value = u'%s'%value
			value = float(value)
	else:
		value = u'0.00'
	try:
		value = locale.currency(value, grouping=True)
	except:
		value = "$0.00"
	return value
	
@register.simple_tag
def systemGoogleAnalytics():
	from r3s_cms.lib.tags import googleAnalytics
	try:
		return googleAnalytics()
	except:
		return ''