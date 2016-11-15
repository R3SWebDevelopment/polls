from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response , redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import Http404 , HttpResponse
from utils import log_exception
import json
import datetime
import csv
import traceback
from r3s_cms.apps.analytics.models import Hit

def render(path = None , content_type = None):
	def render_with_decorator(view_func):
		def wrapper(*args, **kwargs):
			request = args[0] or None
			Hit.page_visited(request = request)
			settings.RESET_DOMAIN = request.META['HTTP_HOST']
			context = view_func(*args, **kwargs)
			if context.__class__ == dict:
				redirect = context.get('redirect') or False
				if redirect:
					url = context.get('url') or None
					if url:
						return HttpResponseRedirect(url)
					else:
						raise Http404
				if content_type == 'json':
					error = context.get('error') or False
					response_data = context.get('response_data') or None
					error_message = ''
					success = True
					if error:
						status = 'error'
						success = False
						exception = context.get('exception') or None
						error_message = log_exception(exception = exception , traceback = traceback.format_exc() , note = _("lib.decorators.render - Error Receive"))
					elif response_data is None:
						status = 'error'
						success = False
						error_message = _('No JSON Data provided')
						exception = Exception(error_message)
						error_message = log_exception(exception = exception , traceback = traceback.format_exc() , note = _("lib.decorators.render - No JSON Data provided"))
					else:
						success = True
						status = 'success'
					timestamp = datetime.datetime.now()
					response_data = {
						'data' : response_data , 
						'status' : status , 
						'timestamp' : str(timestamp) ,
						'error_message' : error_message ,
						'success' : success ,
						'error' : not success,
					}
					return HttpResponse(json.dumps(response_data), content_type="application/json")
				elif content_type == 'csv':
					error = context.get('error') or False
					if error:
						status = 'error'
						exception = context.get('exception') or None
						error_message = log_exception(exception = exception , traceback = traceback.format_exc() , note = _("lib.decorators.render - Error Receive"))
						url = reverse('system_error')
						return HttpResponseRedirect(url)
					csv_header = context.get('csv_header') or None
					csv_body = context.get('csv_body') or None
					if csv_header or csv_body:
						raise Http404
					csv_filename = context.get('csv_filename') or None
					response = HttpResponse(content_type='text/csv')
					response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (csv_filename)
					writer = csv.writer(response)
					writer.writerow(csv_header)
					for row in csv_body:
						writer.writerow(row)
					return response
				elif content_type == 'html':
					error = context.get('error') or False
					if error:
						status = 'error'
						exception = context.get('exception') or None
						error_message = log_exception(exception = exception , traceback = traceback.format_exc() , note = _("lib.decorators.render - Error Receive"))
						url = "%s?error_message=%s" % (reverse('system_error') , error_message)
						return HttpResponseRedirect(url)
					if path:
						return render_to_response(
							path, 
							context, 
							context_instance=RequestContext(request),
						)
			error_message = _('System Error')
			exception = Exception(error_message)
			error_message = log_exception(exception = exception , traceback = traceback.format_exc() , note = _("lib.decorators.render - System Error"))
			url = reverse('system_error')
			return HttpResponseRedirect(url)
		return wrapper
	return render_with_decorator