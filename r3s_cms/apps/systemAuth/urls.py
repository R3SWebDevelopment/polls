from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
	url(r'/log/in/$' , auth_log_in , name = 'auth_log_in') ,
	url(r'/log/in/deactive/$' , auth_log_in_deactive , name = 'auth_log_in_deactive') ,
	url(r'/log/in/submit/$' , auth_log_in_submit , name = 'auth_log_in_submit') ,
	url(r'/log/out/$' , auth_log_out , name = 'auth_log_out') ,
	url(r'/log/reset_password/$' , auth_log_reset_password , name = 'auth_log_reset_password') ,
	url(r'/log/reset_password/submit/$' , auth_log_reset_password_submit , name = 'auth_log_reset_password_submit') ,
	url(r'/groups/$' , auth_groups , name = 'auth_groups') ,
	url(r'/groups/create/$' , auth_groups_create , name = 'auth_groups_create') ,
	url(r'/groups/create/submit/$' , auth_groups_create_submit , name = 'auth_groups_create_submit') ,
	url(r'/groups/(?P<group_id>\w+)/$' , auth_groups_view , name = 'auth_groups_view') ,
	url(r'/groups/(?P<group_id>\w+)/edit/$' , auth_groups_edit , name = 'auth_groups_edit') ,
	url(r'/groups/(?P<group_id>\w+)/edit/submit/$' , auth_groups_edit_submit , name = 'auth_groups_edit_submit') ,
	url(r'/my_account/$' , auth_my_account , name = 'auth_my_account') ,
	url(r'/my_account/edit/$' , auth_my_account_edit , name = 'auth_my_account_edit') ,
	url(r'/my_account/edit/submit/$' , auth_my_account_edit_submit , name = 'auth_my_account_edit_submit') ,
	url(r'/sign-up/$' , auth_sign_up , name = 'auth_sign_up') ,
	url(r'/sign-up/submit/$' , auth_sign_up_submit , name = 'auth_sign_up_submit') ,
	url(r'/sign-up/confirm/$' , auth_sign_up_confirm , name = 'auth_sign_up_confirm') ,
	url(r'/users/$' , auth_users , name = 'auth_users') ,
	url(r'/users/create/$' , auth_users_create , name = 'auth_users_create') ,
	url(r'/users/create/submit/$' , auth_users_create_submit , name = 'auth_users_create_submit') ,
	url(r'/users/(?P<username>\w+)/$' , auth_users_view , name = 'auth_users_view') ,
	url(r'/users/(?P<username>\w+)/edit/$' , auth_users_edit , name = 'auth_users_edit') ,
	url(r'/users/(?P<username>\w+)/edit/submit/$' , auth_users_view_edit_submit , name = 'auth_users_view_edit_submit') ,
	url(r'/users/(?P<username>\w+)/reset_password/$' , auth_users_reset_password , name = 'auth_users_reset_password') ,
)