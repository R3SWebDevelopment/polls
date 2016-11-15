# -*- coding: utf-8 -*-
from r3s_cms.lib import render

def auth(template = None , content_type = None , **kwargs):
	path = 'auth'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)

@auth(template = 'login/form.html' , content_type = 'html')
def auth_log_in(request):
	return {}

@auth(template = 'login/deactive.html' , content_type = 'html')
def auth_log_in_deactive(request):
	return {}

def auth_log_in_submit(request):
	return {}

def auth_log_out(request):
	return {}

@auth(template = 'login/reset_password.html' , content_type = 'html')
def auth_log_reset_password(request):
	return {}

def auth_log_reset_password_submit(request):
	return {}

@auth(template = 'groups/list.html' , content_type = 'html')
def auth_groups(request):
	return {}

@auth(template = 'groups/create.html' , content_type = 'html')
def auth_groups_create(request):
	return {}

def auth_groups_create_submit(request):
	return {}

@auth(template = 'groups/view.html' , content_type = 'html')
def auth_groups_view(request , group_id = None):
	return {}

@auth(template = 'groups/edit.html' , content_type = 'html')
def auth_groups_edit(request , group_id = None):
	return {}

def auth_groups_edit_submit(request):
	return {}

@auth(template = 'users/view.html' , content_type = 'html')
def auth_my_account(request):
	return {
		'error' : True , 
	}

@auth(template = 'users/edit.html' , content_type = 'html')
def auth_my_account_edit(request):
	return {}

def auth_my_account_edit_submit(request):
	return {}

@auth(template = 'sign_up/form.html' , content_type = 'html')
def auth_sign_up(request):
	return {}

def auth_sign_up_submit(request):
	return {}

@auth(template = 'sign_up/confirm_form.html' , content_type = 'html')
def auth_sign_up_confirm(request):
	return {}

@auth(template = 'users/list.html' , content_type = 'html')
def auth_users(request):
	return {}

@auth(template = 'users/create.html' , content_type = 'html')
def auth_users_create(request):
	return {}

def auth_users_create_submit(request):
	return {}

@auth(template = 'users/view.html' , content_type = 'html')
def auth_users_view(request , username = None):
	return {}

@auth(template = 'users/edit.html' , content_type = 'html')
def auth_users_edit(request , username = None):
	return {}

def auth_users_view_edit_submit(request):
	return {}

@auth(template = 'users/reset_password.html' , content_type = 'html')
def auth_users_reset_password(request , username = None):
	return {}