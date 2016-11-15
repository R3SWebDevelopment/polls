# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from r3s_cms.apps.system.models import ProxyUser
from r3s_cms.apps.polls.models import Poll
from r3s_cms.lib.utils import getUser

register = template.Library()

@register.simple_tag
def dashboad_business_label():
	try:
		return '%s' % settings.BUSINESS_LABEL or 'R3S_CMS'
	except:
		return '%s Site Dashboard' % 'R3S_CMS'
		

@register.assignment_tag(takes_context=True)
def dashboard_menu(context , currentSection = None):
	request = context['request'] or None
	if request:
		user = getUser(request)
	else:
		user = None
	menu = [
		{ 'url' : reverse('system_dashboard') , 'section' : 'dashboard' , 'label' : 'Dashboard' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#####################POLLS SYSTEM
#		{ 'url' : reverse('system_polls_test_inventario_talento') , 'section' : 'polls' , 'label' : 'Fase I: Inventario de Talento' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_mapeo_situacional') , 'section' : 'polls' , 'label' : 'Fase I: Mapeo Situacional' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_analisis_desempegno') , 'section' : 'polls' , 'label' : 'Fase I: Análisis del Desempeño' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_pre_coaching') , 'section' : 'polls' , 'label' : 'Fase II: Pre-Coaching' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_sesion_1') , 'section' : 'polls' , 'label' : 'Fase III: Sesión 1' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_sesion_2') , 'section' : 'polls' , 'label' : 'Fase III: Sesión 2' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_sesion_3') , 'section' : 'polls' , 'label' : 'Fase III: Sesión 3' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_sesion_4') , 'section' : 'polls' , 'label' : 'Fase III: Sesión 4' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_sesion_5') , 'section' : 'polls' , 'label' : 'Fase III: Sesión 5' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_sesion_6') , 'section' : 'polls' , 'label' : 'Fase III: Sesión 6' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_analisis_avances') , 'section' : 'polls' , 'label' : 'Fase IV: Análisis Avances' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_polls_test_reporte_final') , 'section' : 'polls' , 'label' : 'Fase V: Reporte Final' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#####################POLLS SYSTEM
		
		
		
#		{ 'url' : reverse('system_dashboard') , 'section' : 'imagery' , 'label' : 'Fotos' , 'icon' : 'fa-picture-o' , 'active' : False , 'has_items' : True , 'items' : [
#																																											{ 'url' : reverse('system_dashboard') ,  'label' : 'Albumes' , 'icon' : 'fa-folder-o' } ,
#																																											{ 'url' : reverse('system_dashboard') ,  'label' : 'Lista' , 'icon' : 'fa-list' } ,
#																																										] } ,
#		{ 'url' : reverse('system_dashboard') , 'section' : 'system' , 'label' : 'Sistema' , 'icon' : 'fa-cogs' , 'active' : False , 'has_items' : True , 'items' : [
#																																											{ 'url' : reverse('system_dashboard') ,  'label' : 'Usuarios' , 'icon' : 'fa-users' } ,
#																																										] } ,
#		{ 'url' : reverse('system_dashboard') , 'section' : 'page_hit' , 'label' : 'Visitas' , 'icon' : 'fa-eye' , 'active' : False , 'has_items' : False , 'items' : [] } ,
#		{ 'url' : reverse('system_dashboard') , 'section' : 'contact_messages' , 'label' : 'Mensajes' , 'icon' : 'fa-comments' , 'active' : False , 'has_items' : False , 'items' : [] } ,
	]
	if user and user.isStaff:
		encuestas = Poll.count()
		menu.append({ 'url' : reverse('system_polls_staff_listing') , 'section' : 'dashboard' , 'label' : 'Encuestras (%s)' % encuestas , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] })
		usuarios = ProxyUser.count()
		menu.append({ 'url' : reverse('system_users') , 'section' : 'dashboard' , 'label' : 'Usuarios (%s)' % usuarios , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] })
		menu.append({ 'url' : reverse('system_questionnaire_stack') , 'section' : 'dashboard' , 'label' : 'Stack de Cuestionarios' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] })
	elif user and not user.isStaff:
		misEncuestas = user.pollCount
		menu.append({ 'url' : reverse('system_polls_my_polls') , 'section' : 'dashboard' , 'label' : 'Mis Encuestas (%s)' % misEncuestas , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] })
#		mensajes = 0
#		menu.append({ 'url' : reverse('system_logout') , 'section' : 'dashboard' , 'label' : 'Mis Mensajes (%s)' % mensajes , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] })
	menu.append({ 'url' : reverse('system_profile') , 'section' : 'dashboard' , 'label' : 'Mi Perfil' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] })
	menu.append({ 'url' : reverse('system_logout') , 'section' : 'dashboard' , 'label' : 'Salir del Sistema' , 'icon' : 'fa-dashboard' , 'active' : False , 'has_items' : False , 'items' : [] })
	return menu
