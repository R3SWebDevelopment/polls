from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import (
										BaseUserManager ,
										AbstractBaseUser ,
										Permission , 
										Group
										)
from r3s_cms.lib.utils import randomStringGenerator
										
class R3SUserManager(BaseUserManager):
	def create_user(self , email = None , username = None , password = None , first_name = None , last_name = None):
		user = None
		if not email:
			msg = _('Users must have an email address')
			raise ValueError(msg)
		if not username:
			msg = _('Users must have an username')
			raise ValueError(msg)
		user = self.model(
						email = email , 
						username = username , 
						first_name = first_name , 
						last_name = last_name
						)
		if not password:
			password = randomStringGenerator(size=10)
			user.passwordSettingNeeded = True
		user.set_password(password)
		user.save(using=self._db)
		return user
		
	def create_staffuser(self , email = None , username = None , password = None , first_name = None , last_name = None):
		user = self.create_user(email = email , username = username , password = password , first_name = first_name , last_name = last_name)
		if user:
			user.is_staff = True
			user.save(using=self._db)
		return user
		
	def create_superuser(self , email = None , username = None , password = None , first_name = None , last_name = None):
		user = self.create_user(email = email , username = username , password = password , first_name = first_name , last_name = last_name)
		if user:
			user.is_superuser = True
			user.save(using=self._db)
		return user
		
class R3SUser(AbstractBaseUser):
	username = models.CharField(unique = True , max_length = 255 , null = False , blank = False)
#	password = models.CharField(max_length = 255 , null = False , blank = False)
	first_name = models.CharField(max_length = 255 , null = True , blank = True)
	last_name = models.CharField(max_length = 255 , null = True , blank = True)
	email = models.EmailField(unique = True , max_length = 255 , null = False , blank = False)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)
	passwordSettingNeeded = models.BooleanField(default = False)
#	last_login = models.DateTimeField(default = None)
	date_joined = models.DateTimeField(auto_now_add = True)
	groups = models.ManyToManyField(Group)
	user_permissions = models.ManyToManyField(Permission)
	
	class Meta:
		permissions = (
						( "create_user", _("Create User") ) ,
						( "change_password", _("Change Password") ) ,
						( "reset_password", _("Reset Password") ) ,
						( "assign_group", _("Assign Proup") ) ,
						( "assign_perms", _("Assign Permission") ) ,
						( "set_user_active", _("Set User Active") ) ,
						( "set_user_inactive", _("Set User Inactive") ) ,
						)
	
	objects = R3SUserManager()
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']
	
	def get_full_name(self):
		if self.first_name and self.last_name:
			name = "%s, %s" % (self.last_name , self.first_name)
		elif self.first_name:
			name = self.first_name
		elif self.last_name:
			name = self.last_name
		else:
			name = ""
		return name
	full_name = property(get_full_name)
		
	def get_short_name(self):
		if self.first_name:
			name = self.first_name
		elif self.last_name:
			name = self.last_name
		else:
			name = ""
		return name
	short_name = property(get_short_name)
	
	def __stf__(self):
		return self.username
		
	def has_perm(self , perm , obj = None):
		if not self.is_active:
			return False
		if perm or perm.__class__ == str:
			perm_list = perm.split('.')
			if len(perm_list) == 2:
				app_label = perm_list[0]
				permission_codename = perm_list[1]
				if app_label or permission_codename:
					permissions = self.get_all_permissions()
					if permissions.objects.filter(content_type__app_label = app_label , codename = permission_codename).exists():
						return True
		return False

	def has_perms(self , perm_list , obj = None):
		for perm in perm_list:
			if not self.has_perm(perm = perm):
				return False
		return True

	def has_module_perms(self , app_label):
		return True
		
	def get_group_permissions(self , obj = None):
		permissions = Permission.objects.none()
		for group in self.groups:
			if group.permissions:
				permissions = permissions|group.permissions
		return permissions
		
	def get_all_permissions(self , obj = None):
		permissions = Permission.objects.none()
		permissions = self.user_permissions
		group_permissions = self.get_group_permissions(obj = obj)
		permissions = permissions|group_permissions
		return permissions

	@classmethod
	def get_users(cls , _all = True , staff = False , superUser = False):
		users = cls.objects.none()
		users = cls.objects.all()
		if _all is False:
			users = cls.objects.exclude(is_active = False)
		staffUsers = users.filter(is_staff = staff)
		superUsers = users.filter(is_superuser = superUser)
		users = staffUsers|superUsers
		return users

	@classmethod
	def get_superUsers(cls , _all = True):
		return cls.get_users(_all = _all , staff = False , superUser = True)

	@classmethod
	def get_staffUsers(cls , _all = True):
		return cls.get_users(_all = _all , staff = True , superUser = False)

	def _isPasswordNeedSetting(self):
		return self.passwordSettingNeeded or False
	isPasswordNeedSetting = property(_isPasswordNeedSetting)

	def passwordSettingRequired(self):
		self.passwordSettingNeeded = True
		self.save()

	def passwordSettingNoRequired(self):
		self.passwordSettingNeeded = False
		self.save()

	def changePassword(self , password = None , confirmPassword = None , passwordSettingNeeded = False):
		if password and confirmPassword and password == confirmPassword:
			self.set_password(password)
			self.save()
			if passwordSettingNeeded:
				self.passwordSettingRequired()
			else:
				self.passwordSettingNoRequired()
		elif password:
			message = _('No Password Provided')
			raise Exception(message)
		elif confirmPassword:
			message = _('No Password Confirmation Provided')
			raise Exception(message)
		elif confirmPassword:
			message = _('No Password Confirmation Provided')
			raise Exception(message)
		elif password != confirmPassword:
			message = _('Password and Password Confirmation Does Not Match')
			raise Exception(message)

	def _hasPendingPasswordReset(self):
		return False
	hasPendingPasswordReset = property(_hasPendingPasswordReset)

	def resetPassword(self):
		if self.hasPendingPasswordReset:
			message = _('This User Has a Password Reset Pending')
			raise Exception(message)
		else:
			newPassword = randomStringGenerator(size=10)
			self.changePassword(self , password = newPassword , confirmPassword = newPassword , passwordSettingNeeded = True)
			passwordResetNotification(email = self.email , password = newPassword)