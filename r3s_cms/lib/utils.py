import string
import random
from django.conf import settings
from r3s_cms.apps.system.models import SystemExceptionLog
from collections import OrderedDict
from r3s_cms.apps.system.models import ProxyUser

def getUser(request):
	user = request.user or None
	if user:
		user = ProxyUser.objects.filter(username = user.get_username()).first()
	if user:
		if user.is_active is False:
			user = None
	return user

def log_exception(exception = None , traceback = None , note = None):
	error_message = None
	if exception:
		try:
			error_message = exception.message
		except:
			error_message = str(exception)
		if not settings.DEBUG:
			log = SystemExceptionLog.log_error(cls , message = error_message , traceback = traceback , note = note)
			if log:
				error_message = log.message
	return error_message

def setForm(fields = []):
	for field in fields:
		fields[field].widget.attrs['class'] = 'form-control'
	return fields

def randomStringGenerator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
	
def lambdaFunction(**kwargs):
	pass

def required_fields(fields , required = []):
	for field in fields:
		if field in required:
			fields[field].required = True
		else:
			fields[field].required = False
	return fields

def reorder_fields(fields, order):
    """Reorder form fields by order, removing items not in order.

    >>> reorder_fields(
    ...     OrderedDict([('a', 1), ('b', 2), ('c', 3)]),
    ...     ['b', 'c', 'a'])
    OrderedDict([('b', 2), ('c', 3), ('a', 1)])
    """
    for key, v in fields.items():
        if key not in order:
            del fields[key]

    return OrderedDict(sorted(fields.items(), key=lambda k: order.index(k[0])))