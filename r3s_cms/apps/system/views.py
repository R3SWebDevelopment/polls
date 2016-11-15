# -*- coding: utf-8 -*-
from r3s_cms.lib import render
from r3s_cms.lib.utils import getUser
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from models import ProxyUser , ProxyGroup , AccessRequest
from r3s_cms.apps.polls.models import Poll , ProxyPoll

def system(template = None , content_type = None , **kwargs):
	path = 'system'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)

@system(template = 'login.html' , content_type = 'html')
def system_login(request):
	user = request.user
	next = request.GET.get('next') or None
	if user and user.is_authenticated():
		return{
			'redirect' : True ,
			'url' : next or reverse('system_dashboard') ,
		}
	return{}

@login_required
@system(template = 'login.html' , content_type = 'html')
def system_logout(request):
	user = request.user
	if user and user.is_authenticated():
		logout(request)
	return{
		'redirect' : True ,
		'url' : reverse('system_login') ,
	}

@require_http_methods(["POST"])	
@system(template = 'login.html' , content_type = 'html')
def system_login_submit(request):
	username = request.POST.get('username') or None
	password = request.POST.get('password') or None
	if username is not None and password is not None:
		user = User.objects.filter(username__iexact = username).first()
		if user is None:
			user = User.objects.filter(email__iexact = username).first()
		if user is not None:
			user = authenticate(username = user.get_username() , password = password)
			if user is not None and user.is_active:
				login(request, user)
				return{
					'redirect' : True ,
					'url' : reverse('system_dashboard') ,
				}
			else:
				return{
					'redirect' : True ,
					'url' : reverse('system_login_error_not_auth') ,
				}
		else:
			return{
				'redirect' : True ,
				'url' : reverse('system_login_error_not_exists') ,
			}
	else:
		return{
			'redirect' : True ,
			'url' : reverse('system_login_error_not_data') ,
		}
		
@system(template = 'login.html' , content_type = 'html')
def system_login_error(request):
	path = request.get_full_path() or None
	if path and len(path.split("?")) > 0:
		path = path.split("?")[0]
		message = ""
		if reverse('system_login_error_not_data') == path:
			message = "Debe de Ingresar Usuario/Contraseña"
		elif reverse('system_login_error_not_exists') == path:
			message = "Usuario No Existe"
		elif reverse('system_login_error_not_auth') == path:
			message = "Acceso No Autorizado"
		else:
			return{
				'exception' : Exception('General Error') ,
				'error' : True ,
			}
	else:
		return{
			'exception' : Exception('General Error') ,
			'error' : True ,
		}
	return{
		'message' : message ,
		'displayMessage' : True ,
	}

@login_required
@system(template = 'polls/stack/list.html' , content_type = 'html')
def system_questionnaire_stack(request):
	PAGE_TITLE = 'Stack de Cuestionarios'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Stack de Cuestionarios' , 'url' : reverse('system_questionnaire_stack') , 'icon' : 'fa-stack-overflow' } , 
	]
	CURRENT_SECTION = 'dashboard'
	questionnaires = ProxyPoll.objects.all()
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'list' : questionnaires ,
	}

@login_required
@system(template = 'polls/stack/view.html' , content_type = 'html')
def system_questionnaire_stack_staff_view(request , poll_id = None):
	if poll_id is None:
		return{
			'exception' : Exception('Cuestionario Encontrado') ,
			'error' : True ,
		}
	questionnaire = ProxyPoll.objects.filter(id = poll_id).first()
	if questionnaire is None:
		return{
			'exception' : Exception('Cuestionario Encontrado') ,
			'error' : True ,
		}
	PAGE_TITLE = 'Stack de Cuestionarios'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Stack de Cuestionarios' , 'url' : reverse('system_questionnaire_stack') , 'icon' : 'fa-stack-overflow' } , 
		{ 'active' : True , 'label' : '%s - %s' % (questionnaire.getSectionName  , questionnaire.getName) , 'url' : questionnaire.viewStaffURL , 'icon' : 'fa-file-text' } , 
	]
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'questionnaire' : questionnaire ,
	}

@login_required
@system(template = 'base/widgets/listing.html' , content_type = 'html')
def system_users(request):
	PAGE_TITLE = 'Usuarios'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
	]
	CURRENT_SECTION = 'dashboard'
	WIDGETS = [
		{
			'icon' : 'fa-users' , 
			'secundaryIcon' : 'fa-user-plus' , 
			'mainLabel' : 'Ver Usuarios' ,
			'secundaryLabel' : 'Agregar Usuario' ,
			'mainUrl': reverse('system_users_list') ,
			'secundaryUrl': reverse('system_users_add') ,
			'counter' : ProxyUser.usersCount() ,
			'type' : None ,
		} ,
		{
			'icon' : 'fa-calendar-o' , 
			'secundaryIcon' : None , 
			'mainLabel' : 'Ver Grupos' ,
			'secundaryLabel' : 'Agregar Grupo' ,
			'mainUrl': reverse('system_users_groups_list') ,
			'secundaryUrl': reverse('system_users_groups_add') ,
			'counter' : ProxyUser.groupsCount() ,
			'type' : 'green' ,
		} ,
		{
			'icon' : 'fa-unlock' , 
			'secundaryIcon' : None , 
			'mainLabel' : 'Ver Administradores' ,
			'secundaryLabel' : 'Agregar Administradores' ,
			'mainUrl': reverse('system_users_staff_list') ,
			'secundaryUrl': reverse('system_users_staff_add') ,
			'counter' : ProxyUser.staffCount() ,
			'type' : 'red' ,
		} ,
		{
			'icon' : 'fa-key' , 
			'secundaryIcon' : None , 
			'mainLabel' : 'Ver Solicitudes de Acceso' ,
			'secundaryLabel' : 'Ver Solicitudes de Acceso' ,
			'mainUrl': reverse('system_users_request_access_list') ,
			'secundaryUrl': reverse('system_users_request_access_list') ,
			'counter' : AccessRequest.count() ,
			'type' : 'yellow' ,
		} ,
	]
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'WIDGETS' : WIDGETS ,
	}

@system(template = 'users/request/add.html' , content_type = 'html')
def system_users_request_access(request):
	submitUrl = reverse('system_users_request_access_submit')
	return{
		'submitUrl' : submitUrl ,
		'firstNameError' : None ,
		'lastNameError' : None ,
		'usernameError' : None ,
		'usernameExistsError' : None ,
		'emailError' : None ,
		'emailExistsError' : None ,
		'confirmEmailError' : None ,
		'firstName' : None ,
		'lastName' : None ,
		'username' : None ,
		'email' : None ,
		'confirmEmail' : None ,
	}

@require_http_methods(["POST"])	
@system(template = 'users/request/add.html' , content_type = 'html')
def system_users_request_access_submit(request):
	firstName = request.POST.get('firstName') or None
	lastName = request.POST.get('lastName') or None
	username = request.POST.get('username') or None
	email = request.POST.get('email') or None
	confirmEmail = request.POST.get('confirmEmail') or None
	submitUrl = reverse('system_users_request_access_submit')
	if firstName and firstName.strip():
		firstNameError = False
	else:
		firstNameError = True
	if lastName and lastName.strip():
		lastNameError = False
	else:
		lastNameError = True
	if username and username.strip():
		usernameError = False
		if ProxyUser.objects.filter(username = username).exists():
			usernameExistsError = True
		else:
			usernameExistsError = False
	else:
		usernameError = True
		usernameExistsError = False
	if email and email.strip():
		emailError = False
		emailExistsError = False
		if confirmEmail and confirmEmail.strip() and email == confirmEmail:
			confirmEmailError = False
		else:
			confirmEmailError = True
	else:
		emailError = True
		emailExistsError = False
		confirmEmailError = True
	if not firstNameError and not lastNameError and not usernameError and not usernameExistsError and not emailError and not emailExistsError and not confirmEmailError:
		try:
			AccessRequest.objects.create(first_name = firstName , last_name = lastName , username = username , email = email)
			return {
				'redirect' : True ,
				'url' : reverse('system_users_request_access_submit_confirmation') ,
			}
		except:
			return {
				'redirect' : True ,
				'url' : reverse('system_users_request_access_submit_error') ,
			}
	return{
		'submitUrl' : submitUrl ,
		'firstNameError' : firstNameError ,
		'lastNameError' : lastNameError ,
		'usernameError' : usernameError ,
		'usernameExistsError' : usernameExistsError ,
		'emailError' : emailError ,
		'emailExistsError' : emailExistsError ,
		'confirmEmailError' : confirmEmailError ,
		'firstName' : firstName ,
		'lastName' : lastName ,
		'username' : username ,
		'email' : email ,
		'confirmEmail' : confirmEmail ,
	}

@system(template = 'users/request/response.html' , content_type = 'html')
def system_users_request_access_submit_response(request , error = False , success = False):
	return {
		'error' : error ,
		'success' : success ,
	}

@login_required
@system(template = 'users/request/list.html' , content_type = 'html')
def system_users_request_access_list(request , staff = False):
	PAGE_SUBTITLE = None
	PAGE_TITLE = 'Solicitudes de Accesso al Sistema'
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
		{ 'active' : True , 'label' : 'Solicitudes de Acceso al Sistema' , 'url' : reverse('system_users_request_access_list') , 'icon' : 'fa-list-ol' } , 
	]
	CURRENT_SECTION = 'dashboard'
	requests = AccessRequest.objects.all()
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'requests' : requests ,
	}

@login_required
@system(template = 'users/request/list.html' , content_type = 'html')
def system_users_request_access_list(request , staff = False):
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
	PAGE_SUBTITLE = None
	PAGE_TITLE = 'Solicitudes de Accesso al Sistema'
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
		{ 'active' : True , 'label' : 'Solicitudes de Acceso al Sistema' , 'url' : reverse('system_users_request_access_list') , 'icon' : 'fa-list-ol' } , 
	]
	CURRENT_SECTION = 'dashboard'
	requests = AccessRequest.objects.all()
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'requests' : requests ,
	}

@login_required
@system(template = 'users/request/list.html' , content_type = 'html')
def system_users_request_access_process(request , request_id = None):
	if request_id is None:
		return {
			'error' : True , 
			'exception' : Exception('Solicitud de Aceso no Encontrada')
		}
	if request_id:
		instance = AccessRequest.objects.filter(id = request_id).first()
		if instance is None:
			return {
				'error' : True , 
				'exception' : Exception('Solicitud de Aceso no Encontrada')
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
	if request.META:
		url = request.META.get('HTTP_REFERER') or reverse('system_users')
	else:
		url = reverse('system_users')
	instance.process
	return{
		'redirect' : True ,
		'url' : url
	}

@login_required
@system(template = 'users/request/list.html' , content_type = 'html')
def system_users_request_access_cancel(request , request_id = None):
	if request_id is None:
		return {
			'error' : True , 
			'exception' : Exception('Solicitud de Aceso no Encontrada')
		}
	if request_id:
		instance = AccessRequest.objects.filter(id = request_id).first()
		if instance is None:
			return {
				'error' : True , 
				'exception' : Exception('Solicitud de Aceso no Encontrada')
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
	if request.META:
		url = request.META.get('HTTP_REFERER') or reverse('system_users')
	else:
		url = reverse('system_users')
	instance.cancel
	return{
		'redirect' : True ,
		'url' : url
	}

@login_required
@system(template = 'users/add.html' , content_type = 'html')
def system_users_add(request , staff = False):
	PAGE_SUBTITLE = None
	if staff:
		PAGE_TITLE = 'Agregar Administrador'
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
			{ 'active' : True , 'label' : 'Agregar Administrador' , 'url' : reverse('system_users_staff_add') , 'icon' : 'fa-user-plus' } , 
		]
		submitUrl = reverse('system_users_staff_add_submit')
	else:
		PAGE_TITLE = 'Agregar Usuario'
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
			{ 'active' : True , 'label' : 'Agregar' , 'url' : reverse('system_users_add') , 'icon' : 'fa-user-plus' } , 
		]
		submitUrl = reverse('system_users_add_submit')
		group_id = request.GET.get('group_id') or None
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'submitUrl' : submitUrl ,
		'group_id' : group_id ,
	}

@require_http_methods(["POST"])	
@login_required
@system(template = 'users/add.html' , content_type = 'html')
def system_users_add_submit(request , staff = False):
	group = None
	user = getUser(request)
	PAGE_SUBTITLE = None
	if staff:
		PAGE_TITLE = 'Agregar Administrador'
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
			{ 'active' : True , 'label' : 'Agregar Administrador' , 'url' : reverse('system_users_staff_add') , 'icon' : 'fa-user-plus' } , 
		]
		submitUrl = reverse('system_users_staff_add_submit')
		url = reverse('system_users_staff_list')
	else:
		PAGE_TITLE = 'Agregar Usuario'
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
			{ 'active' : True , 'label' : 'Agregar' , 'url' : reverse('system_users_add') , 'icon' : 'fa-user-plus' } , 
		]
		submitUrl = reverse('system_users_add_submit')
		url = reverse('system_users_list')
	CURRENT_SECTION = 'dashboard'
	firstName = request.POST.get('firstName') or None
	lastName = request.POST.get('lastName') or None
	username = request.POST.get('username') or None
	email = request.POST.get('email') or None
	confirmEmail = request.POST.get('confirmEmail') or None
	if firstName and firstName.strip() and lastName and lastName.strip() and username and username.strip() and email and email.strip() and confirmEmail and confirmEmail.strip() and email == confirmEmail:
		if staff:
			viewUser = User.objects.create_superuser(username, email, email)
		else:
			viewUser = User.objects.create_user(username, email, email)
			group_id = request.POST.get('group_id') or None
			if group_id is not None and group_id.strip():
				group = ProxyGroup.objects.filter(id = group_id).first()
		if viewUser:
			viewUser.last_name = lastName
			viewUser.first_name = firstName
			viewUser.save()
			viewUser = ProxyUser.objects.filter(username = viewUser.username).first()
			if group is not None:
				viewUser.groups.add(group)
				viewUser.save()
				url = group.viewURL
			return {
				'redirect' : True ,
				'url' : url ,
#				'url' : viewUser.viewURL ,
			}
		return {
			'error' : True , 
			'exception' : Exception('Error Al Crear Usuario') ,
		}
	else:
		if firstName is None:
			firstNameError = True
		else:
			firstNameError = False
		if lastName is None:
			lastNameError = True
		else:
			lastNameError = False
		if username is None:
			usernameError = True
		else:
			usernameError = False
			usernameExistsError = False
		if email is None:
			emailError = True
		else:
			emailError = False
			emailExistsError = False
		if confirmEmail is None:
			confirmEmailError = True
		else:
			confirmEmailError = False
			if email == confirmEmail:
				confirmedEmailError = False
			else:
				confirmedEmailError = True
		return{
			'PAGE_TITLE' : PAGE_TITLE , 
			'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
			'BREADCRUMBS' : BREADCRUMBS , 
			'CURRENT_SECTION' : CURRENT_SECTION ,
			'submitUrl' : reverse('system_users_add_submit') ,
			'firstNameError' : firstNameError ,
			'lastNameError' : lastNameError ,
			'usernameError' : usernameError ,
			'usernameExistsError' : usernameExistsError ,
			'emailError' : emailError ,
			'emailExistsError' : emailExistsError ,
			'confirmEmailError' : confirmEmailError ,
			'confirmedEmailError' : confirmedEmailError ,
		}

@login_required
@system(template = 'users/view.html' , content_type = 'html')
def system_users_view(request , username = None  , staff = False , profile = False):
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	if profile:
		viewUser = ProxyUser.objects.filter(id = user.id).first()
		staff = viewUser.isStaff
	else:
		viewUser = ProxyUser.objects.filter(id = username).first()
	if viewUser is None:
		return{
			'error' : True , 
			'exception' : Exception('Usuario No Encontrado') ,
		}
	edit = False
	superEdit = False
	if user is None:
		return{
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}
	elif user.is_superuser or user.is_staff:
		edit = True
		superEdit = True
	elif user == viewUser:
		edit = True
		superEdit = False
	PAGE_TITLE = '%s' % viewUser.get_full_name()
	PAGE_SUBTITLE = None
	if profile:
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : True , 'label' : viewUser.get_full_name() or 'Ver' , 'url' : reverse('system_profile') , 'icon' : 'fa-user' } , 
		]		
	else:
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
			{ 'active' : True , 'label' : viewUser.get_full_name() or 'Ver' , 'url' : viewUser.viewURL , 'icon' : 'fa-user' } , 
		]
	CURRENT_SECTION = 'dashboard'
	if profile:
		submitUrl = reverse('system_profile_submit')
	else:
		submitUrl = viewUser.submitURL
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'user' : viewUser ,
		'edit' : edit ,
		'superEdit' : superEdit ,
		'submitUrl' : submitUrl ,
		'staff' : staff ,
	}

@login_required
@system(template = 'users/view.html' , content_type = 'html')
def system_users_status_active(request , username = None):
	user = getUser(request)
	viewUser = ProxyUser.objects.filter(id = username).first()
	if request.META:
		url = request.META.get('HTTP_REFERER') or reverse('system_users')
	else:
		url = reverse('system_users')
	if viewUser and viewUser.is_active is False and user and user.is_staff and user.is_superuser and user != viewUser:
		viewUser.is_active = True
		viewUser.save()
	return{
		'redirect' : True ,
		'url' : url ,
	}

@login_required
@system(template = 'users/view.html' , content_type = 'html')
def system_users_status_deactive(request , username = None):
	user = getUser(request)
	viewUser = ProxyUser.objects.filter(id = username).first()
	if request.META:
		url = request.META.get('HTTP_REFERER') or reverse('system_users')
	else:
		url = reverse('system_users')
	if viewUser and viewUser.is_active is True and user and user.is_staff and user.is_superuser and user != viewUser:
		viewUser.is_active = False
		viewUser.save()
	return{
		'redirect' : True ,
		'url' : url ,
	}

@login_required
@system(template = 'users/view.html' , content_type = 'html')
def system_users_reset_password(request , username = None):
	user = getUser(request)
	viewUser = ProxyUser.objects.filter(id = username).first()
	if request.META:
		url = request.META.get('HTTP_REFERER') or reverse('system_users')
	else:
		url = reverse('system_users')
	if viewUser and user and user.is_staff and user.is_superuser:
		viewUser.resetPassword
	return{
		'redirect' : True ,
		'url' : url ,
	}

@require_http_methods(["POST"])	
@login_required
@system(template = 'users/view.html' , content_type = 'html')
def system_users_submit(request , username = None , staff = False , profile = False):
	goBack = True
	email = request.POST.get('email') or None
	password = request.POST.get('password') or None
	confirmPassword = request.POST.get('confirmPassword') or None
	confirmPasswordError = False
	passwordError = False
	passwordChanged = False
	emailError = False
	emailExistsError = False
	groups = request.POST.get('groups') or None	
	user = getUser(request)
	if user is None:
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	if profile:
		viewUser = ProxyUser.objects.filter(id = user.id).first()
		staff = viewUser.isStaff
	else:
		viewUser = ProxyUser.objects.filter(id = username).first()
	if viewUser is None:
		return {
			'error' : True , 
			'exception' : Exception('Usuario No Encontrado')
		}
	edit = False
	superEdit = False
	if user.isStaff:
		edit = True
		superEdit = True
	elif user == viewUser:
		edit = True
		superEdit = False
	if edit is False and superEdit is False :
		return {
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina')
		}
	if edit:
		if email and email.strip():
			if viewUser.email != email:
				viewUser.email = email
				viewUser.save()
		if password and password.strip():
			if len(password) >= 8:
				if confirmPassword and confirmPassword.strip() and confirmPassword == password :
					viewUser.set_password(password)
					viewUser.save()
					passwordChanged = True
				else:
					confirmPasswordError = True
					goBack = False
			else:
				passwordError = True
				goBack = False
	if superEdit:
		viewUser.setGroups(groups = groups)
	if goBack and profile:
		return{
			'redirect' : True ,
			'url' : reverse('system_dashboard')  ,
		}
	elif goBack and not profile:
		return{
			'redirect' : True ,
			'url' : reverse('system_users')  ,
		}
	PAGE_TITLE = '%s' % viewUser.get_full_name()
	PAGE_SUBTITLE = None
	if profile:
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : True , 'label' : viewUser.get_full_name() or 'Ver' , 'url' : reverse('system_profile') , 'icon' : 'fa-user' } , 
		]
	else:
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
			{ 'active' : True , 'label' : viewUser.get_full_name() or 'Ver' , 'url' : viewUser.viewURL , 'icon' : 'fa-user' } , 
		]
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'user' : viewUser ,
		'edit' : edit ,
		'superEdit' : superEdit ,
		'confirmPasswordError' : confirmPasswordError ,
		'passwordError' : passwordError ,
		'passwordChanged' : passwordChanged ,
		'emailError' : emailError ,
		'emailExistsError' : emailExistsError ,
		'staff' : staff ,
	}

@login_required
@system(template = 'users/list.html' , content_type = 'html')
def system_users_list(request , staff = False):
	user = getUser(request)
	if staff:
		PAGE_TITLE = 'Lista de Adminsitradores'
		PAGE_SUBTITLE = None
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
			{ 'active' : True , 'label' : 'Listado de Administradores' , 'url' : reverse('system_users_staff_list') , 'icon' : 'fa-list-ol' } , 
		]
		CURRENT_SECTION = 'dashboard'
		users = ProxyUser.staff.all()
		add_button_label = 'Agregar Administrador'
		add_button_action = reverse('system_users_staff_add')
	else:
		PAGE_TITLE = 'Lista de Usuarios'
		PAGE_SUBTITLE = None
		BREADCRUMBS = [
			{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
			{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
			{ 'active' : True , 'label' : 'Listado de Usuarios' , 'url' : reverse('system_users_list') , 'icon' : 'fa-list-ol' } , 
		]
		CURRENT_SECTION = 'dashboard'
		users = ProxyUser.members.all()
		add_button_label = 'Agregar Usuario'
		add_button_action = reverse('system_users_add')
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'users' : users ,
		'is_staff' : user.isStaff ,
		'add_button_action' : add_button_action ,
		'add_button_label' : add_button_label ,
	}

@login_required
@system(template = 'users/groups/list.html' , content_type = 'html')
def system_users_groups_list(request):
	user = getUser(request)
	PAGE_TITLE = 'Lista de Grupos'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
		{ 'active' : True , 'label' : 'Lista de Grupos' , 'url' : reverse('system_users_groups_list') , 'icon' : 'fa-calendar-o' } , 
	]
	CURRENT_SECTION = 'dashboard'
	groups = ProxyUser.getGroups()
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'groups' : groups ,
		'is_staff' : user.isStaff ,
	}

@login_required
@system(template = 'users/groups/view.html' , content_type = 'html')
def system_users_groups_view(request , group = None):
	user = getUser(request)
	group = ProxyGroup.objects.filter(id = group).first()
	if group is None:
		return{
			'error' : True , 
			'exception' : Exception('Grupo No Encontrado') ,
		}
	if user is None:
		return{
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}
	elif user.isStaff is False:
		return{
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}

	PAGE_TITLE = '%s' % group.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
		{ 'active' : True , 'label' : group.name or 'Ver' , 'url' : group.viewURL , 'icon' : 'fa-calendar-o' } , 
	]
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'submitUrl' : group.submitURL ,
		'group' : group ,
	}

@require_http_methods(["POST"])	
@login_required
@system(template = 'users/groups/view.html' , content_type = 'html')
def system_users_groups_view_submit(request , group = None):
	user = getUser(request)
	group = ProxyGroup.objects.filter(id = group).first()
	goBack = True
	if group is None:
		return{
			'error' : True , 
			'exception' : Exception('Grupo No Encontrado') ,
		}
	if user is None:
		return{
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}
	elif user.isStaff is False:
		return{
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}
	name = request.POST.get('name') or None
	groupError = False
	groupExistsError = False
	if name and name.strip():
		name = name.upper()
		if ProxyGroup.objects.exclude(id = group.id).filter(name__iexact = name).exists():
			groupExistsError = True
			goBack = False
		else:
			group.name = name
			group.save()
	else:
		groupError = True
		goBack = False
	if goBack:
		return {
			'redirect' : True ,
			'url' : reverse('system_users') ,
		}
	PAGE_TITLE = '%s' % group.name
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
		{ 'active' : True , 'label' : group.name or 'Ver' , 'url' : group.viewURL , 'icon' : 'fa-calendar-o' } , 
	]
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'submitUrl' : group.submitURL ,
		'group' : group ,
		'groupExistsError' : groupExistsError ,
		'groupError' : groupError ,
	}

@login_required
@system(template = 'users/groups/add.html' , content_type = 'html')
def system_users_groups_add(request):
	user = getUser(request)
	if user is None:
		return{
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}
	elif user.isStaff is False:
		return{
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}

	PAGE_TITLE = 'Agregar Grupo'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
		{ 'active' : True , 'label' : 'Agregar Grupo' , 'url' : reverse('system_users_groups_add') , 'icon' : 'fa-calendar-plus-o' } , 
	]
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'submitUrl' : reverse('system_users_groups_add_submit') ,
	}

@login_required
@system(template = 'users/groups/add.html' , content_type = 'html')
def system_users_groups_add_submit(request):
	goBack = False
	user = getUser(request)
	if user is None:
		return{
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}
	elif user.isStaff is False:
		return{
			'error' : True , 
			'exception' : Exception('No Tiene Autorizacion Para Ver Esta Pagina') ,
		}
	name = request.POST.get('name') or None
	groupError = False
	groupExistsError = False
	if name and name.strip():
		name = name.upper()
		if ProxyGroup.objects.filter(name__iexact = name).exists():
			groupExistsError = True
		else:
			group = ProxyGroup.objects.create(name = name)
			return {
				'redirect' : True ,
				'url' : group.viewURL ,
			}
	else:
		groupError = True
	if goBack:
		return {
			'redirect' : True ,
			'url' : reverse('system_users') ,
		}
	PAGE_TITLE = 'Agregar Grupo'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Usuarios' , 'url' : reverse('system_users') , 'icon' : 'fa-users' } , 
		{ 'active' : True , 'label' : 'Agregar Grupo' , 'url' : reverse('system_users_groups_add') , 'icon' : 'fa-calendar-plus-o' } , 
	]
	CURRENT_SECTION = 'dashboard'
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'submitUrl' : reverse('system_users_groups_add') ,
		'groupExistsError' : groupExistsError ,
		'groupError' : groupError ,
	}

#@login_required
@system(template = 'users/add.html' , content_type = 'json')
def system_users_verify_email(request):
	error = False
	exception = None
	response_data = {}
	email = request.GET.get('email') or None
	if email:
		exists = ProxyUser.emailExists(email = email)
		response_data = {
			'exists' : exists ,
			'email' : email ,
		}
	else:
		error = True
		exception = Exception('Sin correo electrónico proporcionada')
	return{
		'error' : error ,
		'exception' : exception , 
		'response_data' : response_data ,
	}

#@login_required
@system(template = 'users/add.html' , content_type = 'json')
def system_users_verify_username(request):
	error = False
	exception = None
	response_data = {}
	username = request.GET.get('username') or None
	if username:
		exists = ProxyUser.usernameExists(username = username)
		response_data = {
			'exists' : exists ,
			'username' : username ,
		}
	else:
		error = True
		exception = Exception('Sin nombre de usuario proporcionada')
	return{
		'error' : error ,
		'exception' : exception , 
		'response_data' : response_data ,
	}

@login_required
#@system(template = 'dashboard/base.html' , content_type = 'html')
@system(template = 'base/widgets/listing.html' , content_type = 'html')
def system_dashboard(request):
	user = getUser(request)
	PAGE_TITLE = 'Dashboard'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : True , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
	]
	CURRENT_SECTION = 'dashboard'
	WIDGETS = []
	if user.isStaff:
		WIDGETS.append({
				'icon' : 'fa-users' , 
				'secundaryIcon' : None , 
				'mainLabel' : 'Ver Usuarios' ,
				'secundaryLabel' : 'Ver Administradores' ,
				'mainUrl': reverse('system_users') ,
				'secundaryUrl': reverse('system_users_staff_list') ,
				'counter' : ProxyUser.count() ,
				'type' : None ,	
			})
		WIDGETS.append({
				'icon' : 'fa-question-circle' , 
				'secundaryIcon' : 'fa-plus-circle' , 
				'mainLabel' : 'Ver Encuestras' ,
				'secundaryLabel' : 'Agregar Encuestas' ,
				'mainUrl': reverse('system_polls_staff_listing') ,
				'secundaryUrl': reverse('system_polls_staff_add') ,
				'counter' : Poll.count() ,
				'type' : 'green' ,
			})
	else:
		WIDGETS.append({
				'icon' : 'fa-question-circle' ,
				'secundaryIcon' : None , 
				'mainLabel' : 'Mis Encuestras' ,
				'secundaryLabel' : 'Ver Encuestas' ,
				'mainUrl': reverse('system_polls_my_polls') ,
				'secundaryUrl': reverse('system_polls_my_polls') ,
				'counter' : user.pollCount ,
				'type' : 'green' ,
			})
		WIDGETS.append({
				'icon' : 'fa-briefcase' ,
				'secundaryIcon' : None , 
				'mainLabel' : 'Encuestras Supervisadas' ,
				'secundaryLabel' : 'Ver Encuestas' ,
				'mainUrl': reverse('system_polls_supervised_polls') ,
				'secundaryUrl': reverse('system_polls_supervised_polls') ,
				'counter' : user.supervisedPollsCount ,
				'type' : 'red' ,
			})

	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'WIDGETS' : WIDGETS ,
	}

@system(template = 'imagery/list.html' , content_type = 'html')
def system_imagery(request):
	from r3s_cms.apps.imagery.models import Album
	PAGE_TITLE = 'Albumes'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : True , 'label' : 'Albumes' , 'url' : reverse('system_imagery') , 'icon' : 'fa-picture-o' } , 
	]
	albums = Album.objects.filter(active = True)
	CURRENT_SECTION = 'imagery'
	image_data = {
		'count' : albums.count() ,
		'titles' : [
			{ 'id' : 'index' , 'label' : 'No.' , 'sorted' : False , 'is_index' : True , 'is_link' : False , 'is_money' : False , 'is_action' : False , 'size' : '' } ,
			{ 'id' : 'name' , 'label' : 'Nombre' , 'sorted' : False , 'is_index' : False , 'is_link' : True , 'is_money' : False , 'is_action' : False , 'size' : '' } ,
			{ 'id' : 'description' , 'label' : 'Descripcion' , 'sorted' : False , 'is_index' : False , 'is_link' : False , 'is_money' : False , 'is_action' : False , 'size' : '' } ,
			{ 'id' : 'image_count' , 'label' : 'No. Imagenes' , 'sorted' : False , 'is_index' : False , 'is_link' : False , 'is_money' : False , 'is_action' : False , 'size' : '' } ,
			{ 'id' : 'actions' , 'label' : '' , 'sorted' : False , 'is_index' : False , 'is_link' : False , 'is_money' : False , 'is_action' : True , 'size' : '' } ,
		] ,
		'rows' : [ { 'name' : { 'label' : album.title , 'url' : reverse('system_imagery_view' , kwargs={ 'album_id' : album.id }) , } , 'description' : { 'label' : album.description , } , 'image_count' : { 'label' : album.imageCount , } , 'actions' : [] , } for album in albums]
	}
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'image_data' : image_data , 
	}

@system(template = 'imagery/view.html' , content_type = 'html')
def system_imagery_add(request):
	PAGE_TITLE = 'Agregar Album'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Albumes' , 'url' : reverse('system_imagery') , 'icon' : 'fa-picture-o' } , 
		{ 'active' : True , 'label' : 'Agregar' , 'url' : reverse('system_imagery_add') , 'icon' : 'fa-plus-circle' } , 
	]
	CURRENT_SECTION = 'imagery'
	from r3s_cms.apps.imagery.forms import AlbumForm
	form = AlbumForm()
	form_submit_label = 'Agregar'
	form_action = reverse('system_imagery_add_submit') 
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'form' : form ,
		'form_submit_label' : form_submit_label ,
		'form_action' : form_action ,
		'viewing' : False ,
	}

@require_http_methods(["POST"])
@system(template = 'imagery/view.html' , content_type = 'html')
def system_imagery_add_submit(request):
	PAGE_TITLE = 'Agregar Album'
	PAGE_SUBTITLE = None
	BREADCRUMBS = [
		{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
		{ 'active' : False , 'label' : 'Albumes' , 'url' : reverse('system_imagery') , 'icon' : 'fa-picture-o' } , 
		{ 'active' : True , 'label' : 'Agregar' , 'url' : reverse('system_imagery_add') , 'icon' : 'fa-plus-circle' } , 
	]
	CURRENT_SECTION = 'imagery'
	from r3s_cms.apps.imagery.forms import AlbumForm
	form = AlbumForm(request.POST)
	if form.is_valid():
		try:
			album = form.save()
			return{
				'redirect' : True ,
				'url' : reverse('system_imagery_view' , kwargs={ 'album_id' : album.id }) ,
			}
		except Exception,e:
			from django.forms.forms import NON_FIELD_ERRORS
			msg = "%s" % e.message
			form._errors[NON_FIELD_ERRORS] = form.error_class([msg])
	form_submit_label = 'Agregar'
	form_action = reverse('system_imagery_add_submit') 
	return{
		'PAGE_TITLE' : PAGE_TITLE , 
		'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
		'BREADCRUMBS' : BREADCRUMBS , 
		'CURRENT_SECTION' : CURRENT_SECTION ,
		'form' : form ,
		'form_submit_label' : form_submit_label ,
		'form_action' : form_action ,
		'viewing' : False ,
	}

@system(template = 'imagery/view.html' , content_type = 'html')
def system_imagery_view(request , album_id = None):
	if album_id:
		from r3s_cms.apps.imagery.models import Album
		album = Album.objects.filter(id = album_id).first()
		if album:
			PAGE_TITLE = 'Album: %s' % album.title
			PAGE_SUBTITLE = album.subtitle or None
			BREADCRUMBS = [
				{ 'active' : False , 'label' : 'Dashboard' , 'url' : reverse('system_dashboard') , 'icon' : 'fa-dashboard' } , 
				{ 'active' : False , 'label' : 'Albumes' , 'url' : reverse('system_imagery') , 'icon' : 'fa-picture-o' } , 
				{ 'active' : True , 'label' : PAGE_TITLE , 'url' : reverse('system_imagery_view' , kwargs={ 'album_id' : album.id })  , 'icon' : 'fa-file-image-o' } , 
			]
			CURRENT_SECTION = 'imagery'
			from r3s_cms.apps.imagery.forms import AlbumForm
			form = AlbumForm(instance = album)
			form_submit_label = 'Save'
			form_action = reverse('system_imagery_add_submit') 
			UPLOAD_ACTION = reverse('system_imagery_upload' , kwargs={ 'album_id' : album.id }) 
			images = album.getImages
			return{
				'PAGE_TITLE' : PAGE_TITLE , 
				'PAGE_SUBTITLE' : PAGE_SUBTITLE ,
				'BREADCRUMBS' : BREADCRUMBS , 
				'CURRENT_SECTION' : CURRENT_SECTION ,
				'form' : form ,
				'form_submit_label' : form_submit_label ,
				'form_action' : form_action ,
				'viewing' : True ,
				'UPLOAD_ACTION' : UPLOAD_ACTION ,
				'images' : album.getImages ,
			}
		else:
			return {
				'error' : True ,
				'exception' : Exception('No Album Found')
			}
	return {
		'error' : True ,
		'exception' : Exception('No Album ID Provided')
	}

@require_http_methods(["POST"])
@system(template = 'base/image-base.html' , content_type = 'html')
def system_imagery_upload(request , album_id = None):
	if album_id:
		from r3s_cms.apps.imagery.models import Album , Image , AlbumImage
		album = Album.objects.filter(id = album_id).first()
		if album:
			albumImage = []
			for file_image in request.FILES.getlist('image[]'):
				try:
					image = Image()
					name = file_image.name
					image.image.save(name , file_image)
					image = album.addImage(image = image)
					if image:
						albumImage.append(image)
				except Exception,e:
					pass
			return{
				'image' : None ,
				'images' : albumImage , 
			}
		else:
			return {
				'error' : True ,
				'exception' : Exception('No Album Found')
			}
	return {
		'error' : True ,
		'exception' : Exception('No Album ID Provided')
	}


@system(template = 'test/bootstrap/general.html' , content_type = 'html')
def system_test_bootstrap_general(request , view = None):
	if view and view.__class__ == unicode and view.upper() == 'FULL_SIZE':
		extend_template = 'full_size.html'
		size = "Full Size"
	elif view and view.__class__ == unicode and view.upper() == 'NORMAL':
		extend_template = 'normal.html'
		size = "Normal"
	else:
		extend_template = 'normal.html'
		size = "Normal"
	return {
		'extend_template' : extend_template ,
		'type' : 'General' ,
		'size' : size ,
	}

@system(template = 'test/bootstrap/desktop.html' , content_type = 'html')
def system_test_bootstrap_desktop(request , view = None):
	if view and view.__class__ == unicode and view.upper() == 'FULL_SIZE':
		extend_template = 'full_size.html'
		size = "Full Size"
	elif view and view.__class__ == unicode and view.upper() == 'NORMAL':
		extend_template = 'normal.html'
		size = "Normal"
	else:
		extend_template = 'normal.html'
		size = "Normal"
	return {
		'extend_template' : extend_template ,
		'type' : 'Desktop' ,
		'size' : size ,
	}

@system(template = 'test/bootstrap/iphone.html' , content_type = 'html')
def system_test_bootstrap_iphone(request , view = None):
	if view and view.__class__ == unicode and view.upper() == 'FULL_SIZE':
		extend_template = 'full_size.html'
		size = "Full Size"
	elif view and view.__class__ == unicode and view.upper() == 'NORMAL':
		extend_template = 'normal.html'
		size = "Normal"
	else:
		extend_template = 'normal.html'
		size = "Normal"
	return {
		'extend_template' : extend_template ,
		'type' : 'iPhone' ,
		'size' : size ,
	}

@system(template = 'test/bootstrap/ipad.html' , content_type = 'html')
def system_test_bootstrap_ipad(request , view = None):
	if view and view.__class__ == unicode and view.upper() == 'FULL_SIZE':
		extend_template = 'full_size.html'
		size = "Full Size"
	elif view and view.__class__ == unicode and view.upper() == 'NORMAL':
		extend_template = 'normal.html'
		size = "Normal"
	else:
		extend_template = 'normal.html'
		size = "Normal"
	return {
		'extend_template' : extend_template ,
		'type' : 'iPad' ,
		'size' : size ,
	}

@system(template = 'test/bootstrap/mobile.html' , content_type = 'html')
def system_test_bootstrap_mobile(request , view = None):
	if view and view.__class__ == unicode and view.upper() == 'FULL_SIZE':
		extend_template = 'full_size.html'
		size = "Full Size"
	elif view and view.__class__ == unicode and view.upper() == 'NORMAL':
		extend_template = 'normal.html'
		size = "Normal"
	else:
		extend_template = 'normal.html'
		size = "Normal"
	return {
		'extend_template' : extend_template ,
		'type' : 'Mobile' ,
		'size' : size ,
	}

@system(template = 'test/bootstrap/tablet.html' , content_type = 'html')
def system_test_bootstrap_tablet(request , view = None):
	if view and view.__class__ == unicode and view.upper() == 'FULL_SIZE':
		extend_template = 'full_size.html'
		size = "Full Size"
	elif view and view.__class__ == unicode and view.upper() == 'NORMAL':
		extend_template = 'normal.html'
		size = "Normal"
	else:
		extend_template = 'normal.html'
		size = "Normal"
	return {
		'extend_template' : extend_template ,
		'type' : 'Tablet' ,
		'size' : size ,
	}


@system(template = 'base/error.html' , content_type = 'html')
def system_error(request , view = None):
	if request.META:
		go_back = request.META.get('HTTP_REFERER') or None
	else:
		go_back = None
	error_message = request.GET.get('error_message') or None
	return {
		'error_message' : error_message ,
		'go_back' : go_back ,
	}