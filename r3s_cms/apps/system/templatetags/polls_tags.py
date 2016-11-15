from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from r3s_cms.apps.polls.models import Poll
from r3s_cms.apps.system.models import ProxyUser

register = template.Library()


@register.assignment_tag(takes_context=True)
def contact_message_count(context , currentSection = None):
	return 0
	
@register.filter
def pollProgress(member = None , poll = None):
	if member and poll:
		progress = poll.getMemberProgress(member = member)
		progress = "%s %%" % progress
		return progress
	return "0 %"
	
@register.filter
def pollCount(member = None , poll = None):
	if member and poll:
		progress = poll.getPollCount(member = member)
		progress = "%s" % progress
		return progress
	return "0"

@register.filter
def pollStatus(member = None , poll = None):
	return "Activa"
	if member and poll:
		progress = poll.getMemberProgress(member = member)
		progress = "%s%%" % progress
		return progress
	return "100%"

@register.filter
def pollProgressURL(member = None , poll = None):
	if member and poll:
		return reverse('system_polls_staff_progress_list' , kwargs={'poll': poll.id , 'member': member.id})
	return ""

@register.filter
def pollSuperviserProgressURL(member = None , poll = None):
	if member and poll:
		return reverse('system_polls_supervised_polls_progress_members_detail' , kwargs={'poll': poll.id , 'member': member.id})
	return ""

@register.filter
def questionnaireProgress(member = None , questionnaire = None):
	if member and questionnaire:
		progress = questionnaire.getProgress(member = member)
		progress = "%s%%" % progress
		return progress
	return "0 %"
	
@register.filter
def questionnaireStatus(member = None , questionnaire = None):
	return "Activa"
	if member and questionnaire:
		progress = questionnaire.getProgress(member = member)
		progress = "%s%%" % progress
	return "0 %"

@register.filter
def pollViewUrl(member = None , poll = None):
	if member and poll:
		return reverse('system_polls_my_polls_view' , kwargs={'poll': poll.id})
	return ""
	
@register.simple_tag
def questionnaireResponseUrl(member = None , poll = None , questionnaire = None):
	if member and poll and questionnaire:
		return reverse('system_polls_my_polls_questionnaire_response' , kwargs={'poll': poll.id , 'questionnaire' : questionnaire.slug })
	return ""

@register.simple_tag
def questionnaireViewUrl(member = None , poll = None , questionnaire = None):
	if member and poll and questionnaire:
		return reverse('system_polls_staff_progress_questionnaire_view' , kwargs={'poll': poll.id , 'member': member.id , 'questionnaire' : questionnaire.slug })
	return ""
	
@register.simple_tag
def questionnaireSupervisedViewUrl(member = None , poll = None , questionnaire = None):
	if member and poll and questionnaire:
		return reverse('system_polls_supervised_polls_progress_questionnaire_view' , kwargs={'poll': poll.id , 'member': member.id , 'questionnaire' : questionnaire.slug })
	return ""