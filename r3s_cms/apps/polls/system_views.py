# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from r3s_cms.lib import render
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.http import Http404
from r3s_cms.lib.utils import getUser
from r3s_cms.apps.system.models import ProxyUser
from models import Poll , ProxyPoll , InventarioTalento , MapeoSituacional , AnalisisDesempegno , PreCoaching , SessionOne , SessionTwo , SessionThree , SessionFour , SessionFive , SessionSix , AnalisisAvances , ReporteFinalCoaching
#from forms import InventarioTalentoForm

def system_polls(template = None , content_type = None , **kwargs):
	path = 'system/polls/templates'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)

def staff_polls(template = None , content_type = None , **kwargs):
	path = 'system/polls/staff'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)
def member_polls(template = None , content_type = None , **kwargs):
	path = 'system/polls/member'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)
############################################################################
################################[ MEMBER VIEWS]#############################
############################################################################
@login_required
@member_polls('list.html' , content_type = 'html')
def system_polls_my_polls(request):
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = 'Encuestas'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Mis Encuestas' , 'url' : reverse('system_polls_my_polls') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	polls = user.polls
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'polls' : polls ,
	}
@login_required
@member_polls('view.html' , content_type = 'html')
def system_polls_my_polls_view(request , poll = None):
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	if poll is None:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Se Ha Encontrado')
		}
	poll = Poll.objects.filter(id = poll).first()
	if poll is None:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Se Ha Encontrado')
		}
	PAGE_TITLE = 'Encuesta: %s' % poll.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Mis Encuestas' , 'url' : reverse('system_polls_my_polls') , 'icon' : 'fa-question-circle' } , 
		{ 'active' : True , 'label' : poll.name , 'url' : poll.viewMemberURL , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
		'questionnaires' : poll.getMemberPollsList(member = user) ,
	}
@login_required
@member_polls('response.html' , content_type = 'html')
def system_polls_my_polls_questionnaire_response(request , poll = None , questionnaire = None):
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}
	if poll is None:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Se Ha Encontrado') ,
		}
	poll = Poll.objects.filter(id = poll).first()

	if poll is None:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Se Ha Encontrado') , 
		}
	if questionnaire is None:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Se Ha Encontrado') , 
		}
	questionnaire = poll.getQuestionnaire(member = user , slug = questionnaire)
	if questionnaire is None:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Se Ha Encontrado') ,
		}
	memberPoll = questionnaire.getMemberPoll(member = user)
	if memberPoll is None:
		questionnaire.createPoll(member = user)
		memberPoll = questionnaire.getMemberPoll(member = user)
	if memberPoll is None:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Se Ha Encontrado') ,
		}
	memberPoll.view
	if not memberPoll.isActive or not memberPoll.isAvailable:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Esta Disponible') ,
		}
	if memberPoll.isCommited:
		return {
			'redirect' : True , 
			'url' : memberPoll.viewURL ,
		}
	PAGE_TITLE = 'Encuesta: %s' % questionnaire.title
	PAGE_SUBTITLE = '%s' % questionnaire.subtitle
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Mis Encuestas' , 'url' : reverse('system_polls_my_polls') , 'icon' : 'fa-question-circle' } , 
		{ 'active' : False , 'label' : poll.name , 'url' : poll.viewMemberURL , 'icon' : 'fa-question-circle' } , 
		{ 'active' : True , 'label' : questionnaire.name , 'url' : reverse('system_polls_my_polls_questionnaire_response' , kwargs={'poll': poll.id , 'questionnaire' : questionnaire.slug }) , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	returnURL = poll.viewMemberURL
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
		'questionnaire' : questionnaire ,
		'memberPoll' : memberPoll ,
		'returnURL' : returnURL ,
	}
@require_http_methods(["POST"])
@login_required
@member_polls('response.html' , content_type = 'html')
def system_polls_my_polls_questionnaire_response_submit(request , poll = None , questionnaire = None):
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}
	if poll is None:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Se Ha Encontrado') ,
		}
	poll = Poll.objects.filter(id = poll).first()
	if poll is None:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Se Ha Encontrado') , 
		}
	if questionnaire is None:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Se Ha Encontrado') , 
		}
	questionnaire = poll.getQuestionnaire(member = user , slug = questionnaire)
	if questionnaire is None:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Se Ha Encontrado') ,
		}
	memberPoll = questionnaire.getMemberPoll(member = user)
	memberPoll.view
	if not memberPoll.isActive or not memberPoll.isAvailable:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Esta Disponible') ,
		}
	if memberPoll.isCommited:
		return {
			'redirect' : True , 
			'url' : memberPoll.viewURL ,
		}
	if not memberPoll.isSaveEnabled or not memberPoll.canBeSaved:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Se Puede Guardar') ,
		}
	formClass = memberPoll.formClass
	if formClass:
		form = formClass(request.POST , instance = memberPoll)
	else:
		return{
			'error' : True ,
			'exception' : Exception('El Cuestionario No Se Pudo Guardar')
		}		
	if form.is_valid():
		memberPoll , saved = form.save()
		if not saved:
			return{
				'error' : True ,
				'exception' : Exception('El Cuestionario No Se Pudo Guardar')
			}
	else:
		return{
			'error' : True ,
			'exception' : Exception('El Cuestionario No Se Pudo Guardar')
		}
	return{
		'redirect' : True ,
		'url' : reverse('system_polls_my_polls_questionnaire_response' , kwargs={'poll': poll.id , 'questionnaire' : questionnaire.slug })
	}


############################################################################
################################[ STAFF VIEWS]##############################
############################################################################
@login_required
@staff_polls('list.html' , content_type = 'html')
def system_polls_staff_listing(request , staff = False):
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = 'Encuestas'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
	]
	if staff:
		BREADCRUMBS.append({ 'active' : True , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' } , )
		polls = Poll.objects.all()
	else:
		BREADCRUMBS.append({ 'active' : True , 'label' : 'Encuestas' , 'url' : reverse('system_polls_supervised_polls') , 'icon' : 'fa-question-circle' } , )
		polls = user.supervisedPolls
		
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'polls' : polls ,
		'user' : user ,
		'staff' : staff ,
	}

@login_required
@staff_polls('add.html' , content_type = 'html')
def system_polls_staff_add(request):
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = 'Agregar Encuesta'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' } , 
		{ 'active' : True , 'label' : 'Agregar Encuesta' , 'url' : reverse('system_polls_staff_add') , 'icon' : 'fa-plus-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'nameError' : None ,
		'nameExistsError' : None ,
		'name' : None ,
		'submitUrl' : reverse('system_polls_staff_add_submit') ,
	}

@require_http_methods(["POST"])	
@login_required
@staff_polls('add.html' , content_type = 'html')
def system_polls_staff_add_submit(request):
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = 'Agregar Encuesta'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' } , 
		{ 'active' : True , 'label' : 'Agregar Encuesta' , 'url' : reverse('system_polls_staff_add') , 'icon' : 'fa-plus-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	name = request.POST.get('name') or None
	if name and name.strip():
		nameError = False
		if Poll.objects.filter(name = name).exists():
			nameExistsError = True
		else:
			nameExistsError = False
			try:
				poll = Poll.objects.create(name = name)
				return {
					'redirect' : True ,
					'url' : poll.viewStaffURL ,
				}
			except:
				pass
	else:
		nameError = True
		nameExistsError = False
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'nameError' : nameError ,
		'nameExistsError' : nameExistsError ,
		'name' : name ,
		'submitUrl' : reverse('system_polls_staff_add') ,
	}

@login_required
@staff_polls('view.html' , content_type = 'html')
def system_polls_staff_view(request , poll = None , staff = False):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff and staff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not staff and not poll.isSuperviser(member = user):
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = '%s' % poll.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
	]
	if staff:
		BREADCRUMBS.append({ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' })
		BREADCRUMBS.append({ 'active' : True , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' })
	else:
		BREADCRUMBS.append({ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_supervised_polls') , 'icon' : 'fa-question-circle' })
		BREADCRUMBS.append({ 'active' : True , 'label' : poll.name , 'url' : poll.viewSuperviserURL , 'icon' : 'fa-sticky-note-o' })
	CURRENT_SECTION = 'dashboard'
	submitUrl = poll.saveStaffURL
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll , 
		'nameError' : None ,
		'nameExistsError' : None ,
		'submitUrl' : submitUrl ,
		'errors' : [] ,
		'staff' : staff ,
	}

@login_required
@staff_polls('members/progress.html' , content_type = 'html')
def system_polls_staff_progress_list(request , poll = None , member = None , staff = False):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff and staff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not staff and not poll.isSuperviser(member = user):
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	if member:
		member = ProxyUser.activeMembers.filter(id = member).first()
	else:
		return {
			'error' : True , 
			'exception' : Exception('El Encuestado No Ha Sido Encontrado')
		}
		
	PAGE_TITLE = '%s' % poll.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
	]
	if staff:
		BREADCRUMBS.append({ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' })
		BREADCRUMBS.append({ 'active' : False , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' })
		BREADCRUMBS.append({ 'active' : True , 'label' : member.get_full_name() , 'url' : poll.getMemberProgressURL(member = member) , 'icon' : 'fa-user' } )
	else:
		BREADCRUMBS.append({ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_supervised_polls') , 'icon' : 'fa-question-circle' })
		BREADCRUMBS.append({ 'active' : False , 'label' : poll.name , 'url' : poll.viewSuperviserURL , 'icon' : 'fa-sticky-note-o' })
		BREADCRUMBS.append({ 'active' : True , 'label' : member.get_full_name() , 'url' : poll.getSuperviserMemberProgressURL(member = member) , 'icon' : 'fa-user' } )
	CURRENT_SECTION = 'dashboard'
	submitUrl = poll.saveStaffURL
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll , 
		'questionnaires' : poll.getMemberPollsList(member = member) ,
		'user': member ,
		'staff' : staff ,
	}

@login_required
@staff_polls('members/view.html' , content_type = 'html')
def system_polls_staff_progress_questionnaire_view(request , poll = None , member = None , questionnaire = None , staff = False):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff and staff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not staff and not poll.isSuperviser(member = user):
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	if member:
		member = ProxyUser.activeMembers.filter(id = member).first()
	else:
		return {
			'error' : True , 
			'exception' : Exception('El Encuestado No Ha Sido Encontrado')
		}		
	if questionnaire is None:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Se Ha Encontrado') , 
		}
	questionnaire = poll.getQuestionnaire(member = member , slug = questionnaire)
	if questionnaire is None:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Se Ha Encontrado') ,
		}
	memberPoll = questionnaire.getMemberPoll(member = member)
	if memberPoll is None:
		questionnaire.createPoll(member = user)
		memberPoll = questionnaire.getMemberPoll(member = member)
	if memberPoll is None:
		return {
			'error' : True , 
			'exception' : Exception('El Cuestionario No Se Ha Encontrado') ,
		}
		
	PAGE_TITLE = 'Encuesta: %s' % questionnaire.title
	PAGE_SUBTITLE = '%s' % questionnaire.subtitle
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
	]
	if staff:
		BREADCRUMBS.append({ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' })
		BREADCRUMBS.append({ 'active' : False , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' })
		BREADCRUMBS.append({ 'active' : False , 'label' : member.get_full_name() , 'url' : poll.getMemberProgressURL(member = member) , 'icon' : 'fa-user' })
		BREADCRUMBS.append({ 'active' : True , 'label' : questionnaire.name , 'url' : questionnaire.getMemberProgressURL(member = member) , 'icon' : 'fa-question-circle' })
	else:
		BREADCRUMBS.append({ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_supervised_polls') , 'icon' : 'fa-question-circle' })
		BREADCRUMBS.append({ 'active' : False , 'label' : poll.name , 'url' : poll.viewSuperviserURL , 'icon' : 'fa-sticky-note-o' })
		BREADCRUMBS.append({ 'active' : False , 'label' : member.get_full_name() , 'url' : poll.getSuperviserMemberProgressURL(member = member) , 'icon' : 'fa-user' } )
		BREADCRUMBS.append({ 'active' : True , 'label' : questionnaire.name , 'url' : questionnaire.getSuperviserMemberProgressURL(member = member) , 'icon' : 'fa-question-circle' })
	CURRENT_SECTION = 'dashboard'
	submitUrl = poll.saveStaffURL
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
#		'poll' : poll , 
#		'questionnaires' : poll.getMemberPollsList(member = member) ,
#		'user': member ,
		
		'poll' : poll ,
		'questionnaire' : questionnaire ,
		'memberPoll' : memberPoll ,
		'viewOnly' : True ,
	}

@require_http_methods(["POST"])
@login_required
@staff_polls('view.html' , content_type = 'html')
def system_polls_staff_logo_upload_submit(request , poll = None):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
		
	logoImage = request.FILES['logoImage'] or None
	if logoImage and poll:
		try:
			poll.logo.save(logoImage.name , logoImage)
		except:
			pass
	return {
		'redirect' : True ,
		'url' : poll.viewStaffURL ,
	}

@require_http_methods(["POST"])
@login_required
@staff_polls('view.html' , content_type = 'html')
def system_polls_staff_submit(request , poll = None):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = '%s' % poll.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' } , 
		{ 'active' : True , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' } , 
	]
	CURRENT_SECTION = 'dashboard'
	name = request.POST.get('name') or None
	if name and name.strip():
		if not Poll.objects.filter(name__iexact = name).exclude(id = poll.id).exists():
			poll.name = name
			poll.save()
			return {
				'redirect' : True ,
				'url' : poll.viewStaffURL ,
			}
		else:
			nameError = False
			nameExistsError = True
	else:
		nameError = True
		nameExistsError = False
	submitUrl = poll.saveStaffURL
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll , 
		'nameError' : nameError ,
		'nameExistsError' : nameExistsError ,
		'submitUrl' : submitUrl ,
		'errors' : [] ,
	}

@login_required
@staff_polls('view.html' , content_type = 'html')
def system_polls_staff_start(request , poll = None):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = '%s' % poll.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' } , 
		{ 'active' : True , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' } , 
	]
	CURRENT_SECTION = 'dashboard'
	name = request.POST.get('name') or None
	submitUrl = poll.saveStaffURL
	if poll.isStartEnabled:
		poll.start
		errors = []
	else:
		errors = [
		]
		if poll.getMembersCount == 0:
			errors.append({
				'membersNeeded' : True ,
			})
		if poll.pollsCount == 0:
			errors.append({
				'pollsNeeded' : True ,
			})
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll , 
		'nameError' : None ,
		'nameExistsError' : None ,
		'submitUrl' : submitUrl ,
		'errors' : errors ,
	}

@login_required
@staff_polls('select-member.html' , content_type = 'html')
def system_polls_staff_select_member(request , poll = None , superviser = False):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = '%s' % poll.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' } , 
		{ 'active' : False , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' } , 
		{ 'active' : True , 'label' : 'Seleccionar Encuestados' , 'url' : poll.staffSelectMembersURL , 'icon' : 'fa-sticky-note-o' } , 
	]
	CURRENT_SECTION = 'dashboard'
	if superviser:
		submitUrl = reverse('system_polls_staff_superviser_member_submit' , kwargs={'poll': poll.id})
		members = poll.getAllMembers
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' } , 
			{ 'active' : False , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' } , 
			{ 'active' : True , 'label' : 'Seleccionar Supervisores' , 'url' : poll.staffSelectSuperviserURL , 'icon' : 'fa-sticky-note-o' } , 
		]
	else:
		submitUrl = reverse('system_polls_staff_select_member_submit' , kwargs={'poll': poll.id})
		members = poll.getAvailableMembers
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' } , 
			{ 'active' : False , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' } , 
			{ 'active' : True , 'label' : 'Seleccionar Encuestados' , 'url' : poll.staffSelectMembersURL , 'icon' : 'fa-sticky-note-o' } , 
		]
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
		'members' : members ,
		'submitUrl' : submitUrl ,
		'backUrl' : poll.viewStaffURL ,
	}

@require_http_methods(["POST"])	
@login_required
@staff_polls('select-member.html' , content_type = 'html')
def system_polls_staff_select_member_submit(request , poll = None , superviser = False):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	members = request.POST.get('members') or ""
	members = members.split(',')
	for member in members:
		try:
			member = int(member)
		except:
			member = None
		user = ProxyUser.activeMembers.filter(id = member).first()
		if user:
			if superviser:
				poll.addSuperviser(user = user)
			else:
				poll.addMember(user = user)
	return{
		'redirect' : True ,
		'url' : poll.viewStaffURL ,
	}

@login_required
@staff_polls('select-member.html' , content_type = 'html')
def system_polls_staff_remove_member(request , poll = None , member = None , superviser = False):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	user = ProxyUser.activeMembers.filter(id = member).first()
	if user:
		if superviser:
			poll.removeSuperviser(user = user)
		else:
			poll.removeMember(user = user)
	if request.META:
		url = request.META.get('HTTP_REFERER') or None
	else:
		url = poll.viewStaffURL
	return{
		'redirect' : True ,
		'url' : url ,
	}

@login_required
@staff_polls('select-poll.html' , content_type = 'html')
def system_polls_staff_select_poll(request , poll = None):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = '%s' % poll.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' } , 
		{ 'active' : False , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' } , 
		{ 'active' : True , 'label' : 'Seleccionar Encuesta' , 'url' : poll.staffSelectPollsURL , 'icon' : 'fa-sticky-note-o' } , 
	]
	submitUrl = reverse('system_polls_staff_select_poll_submit' , kwargs={'poll': poll.id})
	CURRENT_SECTION = 'dashboard'
	polls = poll.getAvailablePolls
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
		'polls' : polls ,
		'submitUrl' : submitUrl ,
		'backUrl' : poll.viewStaffURL ,
	}

@require_http_methods(["POST"])	
@login_required
@staff_polls('select-member.html' , content_type = 'html')
def system_polls_staff_select_poll_submit(request , poll = None):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	members = request.POST.get('members') or ""
	members = members.split(',')
	for member in members:
		try:
			member = int(member)
		except:
			member = None
		instance = ProxyPoll.objects.filter(id = member).first()
		if instance:
			poll.addPoll(poll = instance)
	return{
		'redirect' : True ,
		'url' : poll.viewStaffURL ,
	}

@login_required
@staff_polls('select-member.html' , content_type = 'html')
def system_polls_staff_remove_poll(request , poll = None , questionnaire = None):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	poll.removePoll(poll = questionnaire)
	if request.META:
		url = request.META.get('HTTP_REFERER') or None
	else:
		url = poll.viewStaffURL
	return{
		'redirect' : True ,
		'url' : url ,
	}

@login_required
@staff_polls('view.html' , content_type = 'html')
def system_polls_staff_progress_members_detail(request , poll = None , member = None , staff = False):
	if poll:
		poll = Poll.objects.filter(id = poll).first()
		if poll is None:
			return {
				'error' : True , 
				'exception' : Exception('La Encuesta No Ha Sido Encontrado')
			}
	else:
		return {
			'error' : True , 
			'exception' : Exception('La Encuesta No Ha Sido Encontrado')
		}
	if member:
		pass
	else:
		return {
			'error' : True , 
			'exception' : Exception('El Encuestado No Ha Sido Encontrado')
		}
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not user.isStaff and staff:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	elif not staff and not poll.isSuperviser(member = user):
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	PAGE_TITLE = '%s' % poll.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
	]
	if staff:
		BREADCRUMBS.append({ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_staff_listing') , 'icon' : 'fa-question-circle' })
		BREADCRUMBS.append({ 'active' : True , 'label' : poll.name , 'url' : poll.viewStaffURL , 'icon' : 'fa-sticky-note-o' })
	else:
		BREADCRUMBS.append({ 'active' : False , 'label' : 'Encuestas' , 'url' : reverse('system_polls_supervised_polls') , 'icon' : 'fa-question-circle' })
		BREADCRUMBS.append({ 'active' : True , 'label' : poll.name , 'url' : poll.viewSuperviserURL , 'icon' : 'fa-sticky-note-o' })
	CURRENT_SECTION = 'dashboard'
	submitUrl = poll.saveStaffURL
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll , 
		'nameError' : None ,
		'nameExistsError' : None ,
		'submitUrl' : submitUrl ,
		'errors' : [] ,
	}

############################################################################
############################################################################
@system_polls('Fase-I/inventario-talento/base.html' , content_type = 'html')
def system_polls_test_inventario_talento(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase I: Inventario de Talento' , 'url' : reverse('system_polls_test_inventario_talento') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = InventarioTalento
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
	
@system_polls('Fase-I/mapeo-situacional/base.html' , content_type = 'html')
def system_polls_test_mapeo_situacional(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase I: Mapeo Situacional' , 'url' : reverse('system_polls_test_mapeo_situacional') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = MapeoSituacional
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-I/analisis-desempegno/base.html' , content_type = 'html')
def system_polls_test_analisis_desempegno(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase I: Análisis del Desempeño' , 'url' : reverse('system_polls_test_analisis_desempegno') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = AnalisisDesempegno
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-II/pre-coaching/base.html' , content_type = 'html')
def system_polls_test_pre_coaching(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase II: Pre-Coaching' , 'url' : reverse('system_polls_test_pre_coaching') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = PreCoaching
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-III/sesion-1/base.html' , content_type = 'html')
def system_polls_test_sesion_1(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase III: Sesion 1' , 'url' : reverse('system_polls_test_sesion_1') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = SessionOne
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-III/sesion-2/base.html' , content_type = 'html')
def system_polls_test_sesion_2(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase III: Sesion 2' , 'url' : reverse('system_polls_test_sesion_2') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = SessionTwo
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-III/sesion-3/base.html' , content_type = 'html')
def system_polls_test_sesion_3(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase III: Sesion 3' , 'url' : reverse('system_polls_test_sesion_3') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = SessionThree
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-III/sesion-4/base.html' , content_type = 'html')
def system_polls_test_sesion_4(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase III: Sesion 4' , 'url' : reverse('system_polls_test_sesion_4') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = SessionFour
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-III/sesion-5/base.html' , content_type = 'html')
def system_polls_test_sesion_5(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase III: Sesion 5' , 'url' : reverse('system_polls_test_sesion_5') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = SessionFive
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-III/sesion-6/base.html' , content_type = 'html')
def system_polls_test_sesion_6(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase III: Sesion 6' , 'url' : reverse('system_polls_test_sesion_6') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = SessionSix
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-IV/analisis-avances/base.html' , content_type = 'html')
def system_polls_test_analisis_avances(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase IV: Análisis Avances' , 'url' : reverse('system_polls_test_analisis_avances') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = AnalisisAvances
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}
@system_polls('Fase-V/reporte-final/base.html' , content_type = 'html')
def system_polls_test_reporte_final(request):
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Fase V: Reporte Final' , 'url' : reverse('system_polls_test_reporte_final') , 'icon' : 'fa-question-circle' } , 
	]
	CURRENT_SECTION = 'dashboard'
	poll = ReporteFinalCoaching
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'poll' : poll ,
	}