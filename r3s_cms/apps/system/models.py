from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from slugify import slugify

class SystemExceptionLog(models.Model):
	created_timestamp = models.DateTimeField(null = True , blank = True , auto_now_add = True)
	note = models.TextField(null = True , blank = True , default = "")
	message = models.TextField(null = True , blank = True , default = "")
	message_aux = models.TextField(null = True , blank = True , default = "")
	traceback = models.TextField(null = True , blank = True , default = "")
	error = models.NullBooleanField(default = False)
	
	@classmethod
	def log_error(cls , message = None , traceback = None , note = None):
		if message and traceback:
			return cls.objects.create(message = message , traceback = traceback , note = note , error = True)
		return None

class ActiveRequest(models.Manager):
    def get_queryset(self):
        return super(ActiveRequest, self).get_queryset().filter(active = True)
class AccessRequest(models.Model):
	first_name = models.CharField(null = False , blank = False , max_length = 250 , editable = False)
	last_name = models.CharField(null = False , blank = False , max_length = 250 , editable = False)
	username = models.CharField(null = False , blank = False , max_length = 250 , editable = False)
	email = models.EmailField(null = False , blank = False , max_length = 250 , editable = False)
	active = models.NullBooleanField(default = True)
	objects = ActiveRequest()
	
	def _process(self):
		if not ProxyUser.objects.filter(username = self.username).exists() and not ProxyUser.objects.filter(email = self.email).exists():
			try:
				viewUser = User.objects.create_user(self.username, self.email, self.email)
				if viewUser:
					viewUser.last_name = self.last_name.title()
					viewUser.first_name = self.first_name.title()
					viewUser.save()
					self.active = False
					self.save()
					self.__class__.objects.filter(email = self.email).update(active = False)
					self.__class__.objects.filter(username = self.username).update(active = False)
					return True
			except:
				pass
		return False
	process = property(_process)
	
	def _cancel(self):
		self.active = False
		self.save()
	cancel = property(_cancel)

	def _name(self):
		return "%s %s" % (self.first_name , self.last_name)
	name = property(_name)

	def _processURL(self):
		return reverse('system_users_request_access_process' , kwargs={'request_id': self.id})
	processURL = property(_processURL)

	def _cancelURL(self):
		return reverse('system_users_request_access_cancel' , kwargs={'request_id': self.id})
	cancelURL = property(_cancelURL)

	@classmethod
	def count(self):
		return self.objects.all().count()

class ActiveMember(models.Manager):
    def get_queryset(self):
        return super(ActiveMember, self).get_queryset().exclude(is_active = False).exclude(is_superuser = True).exclude(is_staff = True)
class Member(models.Manager):
    def get_queryset(self):
        return super(Member, self).get_queryset().exclude(is_superuser = True).exclude(is_staff = True)
class ActiveStaff(models.Manager):
    def get_queryset(self):
        return super(ActiveStaff, self).get_queryset().exclude(is_active = False).filter(is_staff = True)
class Staff(models.Manager):
    def get_queryset(self):
        return super(Staff, self).get_queryset().filter(is_staff = True)
class ActiveSuperUser(models.Manager):
    def get_queryset(self):
        return super(ActiveSuperUser, self).get_queryset().exclude(is_active = False).filter(is_superuser = True)
class SuperUser(models.Manager):
    def get_queryset(self):
        return super(SuperUser, self).get_queryset().filter(is_superuser = True)
class ProxyUser(User):
	activeMembers = ActiveMember()
	members = Member()
	activeStaff = ActiveStaff()
	staff = Staff()
	activesuperUser = ActiveSuperUser()
	superUser = SuperUser()
	class Meta:
		proxy = True
		ordering = ['username']

	def _resetPassword(self):
		if self.email:
			self.set_password(self.email)
			self.save()
	resetPassword = property(_resetPassword)
	
	def _getGroups(self):
		groups = [ group.name for group in self.groups.all()]
		groups = ", ".join(groups)
		return groups
	getGroup = property(_getGroups)
	
	def _getGroupsList(self):
		groups = [ group.name for group in self.groups.all()]
		return groups
	getGroupsList = property(_getGroupsList)
	
	def setGroups(self , groups = None):
		groupsData = []
		if groups and groups.__class__ == dict:
			groupsData = groups
		elif groups and (groups.__class__ == str or groups.__class__ == unicode):
			groupsData = groups.split(",")
		self.groups.clear()
		self.save()
		for group in groupsData:
			group = group.upper()
			instance , created = Group.objects.get_or_create(name = group)
			self.groups.add(instance)
			self.save()
	
	def _isStaff(self):
		return self.is_active and self.is_staff and self.is_superuser
	isStaff = property(_isStaff)

	def _viewURL(self):
#		username = slugify(self.id , separator='_')
		username = self.id
		if self.isStaff:
			return reverse('system_users_staff_view' , kwargs={'username': username})
		return reverse('system_users_view' , kwargs={'username': username})
	viewURL = property(_viewURL)

	def _submitURL(self):
#		username = slugify(self.id , separator='_')
		username = self.id
		return reverse('system_users_submit' , kwargs={'username': username})
	submitURL = property(_submitURL)

	def _activeURL(self):
#		username = slugify(self.id , separator='_')
		username = self.id
		return reverse('system_users_status_active' , kwargs={'username': username})
	activeURL = property(_activeURL)

	def _deactiveURL(self):
#		username = slugify(self.id , separator='_')
		username = self.id
		return reverse('system_users_status_deactive' , kwargs={'username': username})
	deactiveURL = property(_deactiveURL)

	def _resetPasswordURL(self):
#		username = slugify(self.id , separator='_')
		username = self.id
		return reverse('system_users_reset_password' , kwargs={'username': username})
	resetPasswordURL = property(_resetPasswordURL)
	
	def _pollCount(self):
		return self.polls.count()
	pollCount = property(_pollCount)
	
	def _supervisedPollsCount(self):
		return self.supervisedPolls.count()
	supervisedPollsCount = property(_supervisedPollsCount)
	
	def _supervisedPolls(self):
		return self.SupervisedPolls.all()
	supervisedPolls = property(_supervisedPolls)
	
	def _polls(self):
		return self.AssignedPolls.all()
	polls = property(_polls)

	@classmethod
	def count(cls):
		return cls.objects.all().count()
		
	@classmethod
	def staffCount(cls):
		return cls.staff.all().count()
		
	@classmethod
	def usersCount(cls):
		return cls.members.all().count()

	@classmethod
	def emailExists(cls , email = None):
		if email is not None and cls.objects.filter(email__iexact = email).exists():
			return True
		return False

	@classmethod
	def usernameExists(cls , username = None):
		if username is not None and cls.objects.filter(username__iexact = username).exists():
			return True
		return False
		
	@classmethod
	def groupsCount(cls):
		return Group.objects.all().count()
		
	@classmethod
	def getGroups(cls):
		return ProxyGroup.objects.all()
		
class ProxyGroup(Group):
	class Meta:
		proxy = True
		ordering = ['name']

	def __unicode__(self):
		return self.name

	def _viewURL(self):
		group = self.id
		return reverse('system_users_groups_view' , kwargs={'group': group})
	viewURL = property(_viewURL)

	def _submitURL(self):
		group = self.id
		return reverse('system_users_groups_view_submit' , kwargs={'group': group})
	submitURL = property(_submitURL)

	def _addNewMemberURL(self):
		return "%s?group_id=%s" % ( reverse('system_users_add') , self.id )		
	addNewMemberURL = property(_addNewMemberURL)

	def _members(self):
		
		return ProxyUser.objects.filter(id__in = [ u.id for u in self.user_set.all() ])
	members = property(_members)