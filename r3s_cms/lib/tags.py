from django.conf import settings
from django.template import loader, Context

def googleAnalyticsEnabled():
	try:
		if not settings.DEBUG and settings.GOOGLE_ANALYTICS:
			return True
	except:
		pass
	return False

def googleAnalytics():
	if googleAnalyticsEnabled():
		template = loader.get_template('googleAnalytics/code.html')
		context = Context({ 'GOOGLE_ID': settings.GOOGLE_GOOGLE_ANALYTICS_ID })
		html = template.render(context)
		return html
	return ""