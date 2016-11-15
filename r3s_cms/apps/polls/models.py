# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import now as timestampNow
from django.core.urlresolvers import reverse
from r3s_cms.apps.system.models import ProxyUser , ProxyGroup
from django.contrib.contenttypes.models import ContentType

##############Manager Definition
class BaseActiveManager(models.Manager):
	def get_queryset(self):
		return super(BaseActiveManager , self).get_queryset().filter(is_active = True)
class BaseCommitedManager(models.Manager):
	def get_queryset(self):
		return super(BaseActiveManager , self).get_queryset().filter(is_commited = True)
class BaseAvailableManager(models.Manager):
	def get_queryset(self):
		return super(BaseActiveManager , self).get_queryset().filter(is_available = True)
class BaseStartedManager(models.Manager):
	def get_queryset(self):
		return super(BaseActiveManager , self).get_queryset().filter(is_started = True)
class ProxyPollManager(models.Manager):

	def get_queryset(self):
		excludeModels = [
			'base' ,
			'poll' ,
			'proxypoll' ,
			'pollquestionnaireassigment' ,
			'it_talento' ,
			'ad_evaluacionindividualcolaboradores' ,
			'ad_seleccioncoachee' ,
			'so_retroalimentacioninicial' ,
			'so_areaoportunidad' ,
			'st_improvementone' ,
			'st_improvementtwo' ,
			'st_actionplan' ,
			'st_accion' ,
			'sf_performance' ,
			'aa_task' ,
		]
		return super(ProxyPollManager , self).get_queryset().filter(app_label__iexact = 'polls').exclude(model__in=excludeModels)
##############Models Definition
class ProxyPoll(ContentType):
	objects = ProxyPollManager()
	class Meta:
		proxy = True
		
	def _ModelClass(self):
		return self.model_class()
	ModelClass = property(_ModelClass)

	def createPoll(self , poll = None , assigment = None , member = None):
		instance = None
		if poll and assigment and member:
			instance = self.model_class().createPoll(poll = poll , assigment = assigment , member = member)
		return instance
		
	def _viewStaffURL(self):
		return reverse('system_questionnaire_stack_staff_view' , kwargs={'poll_id': self.id})
	viewStaffURL = property(_viewStaffURL)

	def _getPollName(self):
		return self.model
	getPollName = property(_getPollName)
	
	def _getName(self):
		return self.model_class().getPollName()
	getName=property(_getName)

	def _getSectionName(self):
		return self.model_class().getPollSectionName()
	getSectionName=property(_getSectionName)

	def _getSortIndex(self):
		return self.model_class().getSortIndex()
	getSortIndex=property(_getSortIndex)
	
	def _questionNumber(self):
		return self.model_class().getTotalQuestions()
	questionNumber = property(_questionNumber)

	def getMemberPoll(self , poll = None , member = None):
		memberPoll = None
		if poll and member:
			memberPoll = self.model_class().objects.filter(user = member , poll = poll).first()
		return memberPoll

	def getProgress(self , poll = None , member = None):
		if poll and member:
			poll = self.model_class().objects.filter(user = member , poll = poll).first()
			if poll:
				return poll.getProgress
		return 0

	def _template(self):
		return self.model_class().template()
	template = property(_template)

class Poll(models.Model):
	name = models.CharField(max_length = 250 , blank = True , null = True)
	completionTime = models.DurationField(null = True)
	supervisers = models.ManyToManyField(ProxyUser , related_name="SupervisedPolls")
	members = models.ManyToManyField(ProxyUser , related_name="AssignedPolls")
##############TIMESTAMPS
	createdTimestamp = models.DateTimeField(auto_now_add = True , null = True)
	availableTimestamp = models.DateTimeField(null = True)
	startedTimestamp = models.DateTimeField(null = True)
	endedTimestamp = models.DateTimeField(null = True)
	deadlineTimestamp = models.DateTimeField(null = True)
	updatedTimestamp = models.DateTimeField(auto_now = True , null = True)
##############FLAGS
	is_active = models.NullBooleanField(default = True)
	is_available = models.NullBooleanField(default = False)
	is_started = models.NullBooleanField(default = False)
	is_ended = models.NullBooleanField(default = False)
	is_deadline = models.NullBooleanField(default = False)
	logo = models.ImageField(upload_to='img/polls/logos/' , blank=True , null=True)
	objects=BaseActiveManager()

	def __unicode__(self):
		return self.__str__()

	def __str__(self):
		return "%s" %(self.name)
		
	def _logoURL(self):
		logoURL = 'https://placehold.it/300?text=Sin+Logo'
		if self.logo:
			logoURL = self.logo.url
		return logoURL
	logoURL = property(_logoURL)
	
	def _hasLogo(self):
		if self.logo:
			return True
		return False
	hasLogo = property(_hasLogo)

	def getMemberProgressURL(self, member = None):
		from r3s_cms.apps.system.templatetags.polls_tags import pollProgressURL
		return pollProgressURL(member = member , poll = self)
	
	def getSuperviserMemberProgressURL(self, member = None):
		from r3s_cms.apps.system.templatetags.polls_tags import pollSuperviserProgressURL
		return pollSuperviserProgressURL(member = member , poll = self)

	def getMemberProgress(self , member = None):
		progress = 0
		count = 0
		if member:
			polls = self.polls
			for poll in polls:
				progress += poll.getProgress(member)
				count += 1
		if count > 0:
			progress = progress/count
		return progress

	def getMemberPolls(self , member = None):
		polls = PollQuestionnaireAssigment.objects.none()
		if member:
			polls = self.polls
			polls = polls.exclude(restrictedMembers = member)
			exclusive = polls.exclude(exclusiveMembers__isnull = True).filter(exclusiveMembers = member)
			regular = polls.exclude(exclusiveMembers__isnull = False)
			if regular.count() > 0 and exclusive.count() > 0:
				polls = regular | exclusive
			elif regular.count() > 0 and exclusive.count() == 0:
				polls = regular
			elif regular.count() == 0 and exclusive.count() > 0:
				polls = exclusive
		return polls

	def getMemberPollsList(self , member = None):
		polls = PollQuestionnaireAssigment.objects.none()
		polls = list(self.polls)
		polls = sorted(polls, key=lambda a: a.getSortIndex)
		return polls

	def getPollCount(self , member = None):
		count = 0
		if member:
			member_id = member.id
			polls = self.getMemberPolls(member = member)
			count = polls.count()
		return count
		
	def getQuestionnaire(self , member = None , slug = None):
		questionnaire = None
		if member and slug:
			polls = self.getMemberPolls(member = member)
			questionnaire = polls.filter(questionnaire = slug).first()
		return questionnaire

	def remove(self):
		self.is_active = False
		self.save()
		
	def _start(self):
		if self.isStartEnabled:
			for q in self.questionnaire.all():
				q.start
			now = timestampNow()
			self.is_available = True
			self.is_started = True
			self.availableTimestamp = now
			self.startedTimestamp = now
			self.save()
	start=property(_start)

	def _status(self):
		status = ""
		if self.is_active and not self.is_available and not self.is_started and not self.is_ended:
			status = "No Iniciada"
		elif self.is_active and self.is_available and self.is_started and not self.is_ended:
			status = "Iniciada"
		elif self.is_active and self.is_available and self.is_started and self.is_ended:
			status = "Finalizada"
		return status
	status = property(_status)
		
	def _isEnabledToRemovePoll(self):
		return True
	isEnabledToRemovePoll = property(_isEnabledToRemovePoll)

	def _isEnabledToAddPoll(self):
		return True
	isEnabledToAddPoll = property(_isEnabledToAddPoll)

	def _isStartEnabled(self):
		if self.is_active and not self.is_available and not self.is_started and not self.is_ended and self.pollsCount > 0 and self.getMembersCount > 0:
			return True
		return False
	isStartEnabled = property(_isStartEnabled)
	
	def _isStarted(self):
		if self.is_active and self.is_available and self.is_started and not self.is_ended and self.pollsCount > 0 and self.getMembersCount > 0:
			return True
		return False
	isStarted = property(_isStarted)

	def _isEnded(self):
		if self.is_active and self.is_available and self.is_started and self.is_ended and self.pollsCount > 0 and self.getMembersCount > 0:
			return True
		return False
	isEnded = property(_isEnded)

	@classmethod
	def count(cls):
		return cls.objects.all().count()

	def addMember(self , user = None):
		self.members.add(user)
		
	def removeMember(self , user = None):
		self.members.remove(user)

	def _getMembers(self):
		return ProxyUser.activeMembers.filter(id__in=[ m.id for m in self.members.all() ])
	getMembers=property(_getMembers)

	def _getMembersCount(self):
		return self.getMembers.count()
	getMembersCount=property(_getMembersCount)

	def addSuperviser(self , user = None):
		self.supervisers.add(user)
		
	def removeSuperviser(self , user = None):
		self.supervisers.remove(user)

	def _getSupervisers(self):
		return self.supervisers.all()
	getSupervisers=property(_getSupervisers)
	
	def isSuperviser(self , member = None):
		if member:
			supervisers = self.getSupervisers
			if supervisers and supervisers.count() > 0 and supervisers.filter(id = member.id).exists():
				return True
		return False
	
	def _getAvailableMembers(self):
		return ProxyUser.activeMembers.exclude(id__in=[ member.id for member in self.getMembers ])
	getAvailableMembers=property(_getAvailableMembers)
	
	def _getAvailableSupervisers(self):
		return ProxyUser.activeStaff.exclude(id__in=[ member.id for member in self.getSupervisers ])
	getAvailableSupervisers=property(_getAvailableSupervisers)
	
	def _getAllMembers(self):
		return ProxyUser.activeMembers.all()
	getAllMembers=property(_getAllMembers)

	def _staffSelectMembersURL(self):
		return reverse('system_polls_staff_select_member' , kwargs={'poll': self.id})
	staffSelectMembersURL=property(_staffSelectMembersURL)

	def _staffSelectSuperviserURL(self):
		return reverse('system_polls_staff_superviser_member' , kwargs={'poll': self.id})
	staffSelectSuperviserURL=property(_staffSelectSuperviserURL)

	def _staffSelectPollsURL(self):
		return reverse('system_polls_staff_select_poll' , kwargs={'poll': self.id})
	staffSelectPollsURL=property(_staffSelectPollsURL)

	def _staffStartPollsURL(self):
		return reverse('system_polls_staff_start' , kwargs={'poll': self.id})
	staffStartPollsURL=property(_staffStartPollsURL)

	def _groups(self):
		return ProxyGroup.objects.all()
	groups = property(_groups)

	def _isEditable(self):
		if self.isStarted:
			return True
		if not self.isEnded:
			return True
		return False
	isEditable=property(_isEditable)
		
	def _statusText(self):
		if self.is_ended:
			return "Finalizada"
		elif self.is_started:
			return "En Proceso"
		elif self.is_available:
			return "Disponible"				
		elif self.is_active:
			return ""
		else:
			return "Eliminada"

	statusText = property(_statusText)
	
	def _viewStaffURL(self):
		return reverse('system_polls_staff_view' , kwargs={'poll': self.id})
	viewStaffURL = property(_viewStaffURL)
	
	def _viewSuperviserURL(self):
		return reverse('system_polls_supervised_polls_view' , kwargs={'poll': self.id})
	viewSuperviserURL = property(_viewSuperviserURL)
	
	def _viewMemberURL(self):
		return reverse('system_polls_my_polls_view' , kwargs={'poll': self.id})
	viewMemberURL = property(_viewMemberURL)
	
	def _saveStaffURL(self):
		return reverse('system_polls_staff_submit' , kwargs={'poll': self.id})
	saveStaffURL = property(_saveStaffURL)

	def _getAvailablePolls(self):
		polls = self.getPolls
		exclude = [ poll.questionnaire or None for poll in self.polls ]
		polls = polls.exclude(model__in = exclude)
		return polls
	getAvailablePolls=property(_getAvailablePolls)
	
	def _getPolls(self):
		polls = ProxyPoll.objects.all()
		return polls
	getPolls=property(_getPolls)
	
	def _polls(self):
		return self.questionnaire.all()
	polls = property(_polls)

	def _pollsCount(self):
		return self.polls.count()
	pollsCount = property(_pollsCount)

	def _pollsList(self):
		polls = list(self.polls)
		polls = sorted(polls, key=lambda a: a.getSortIndex)
		return polls
	pollsList = property(_pollsList)
	
	def addPoll(self , poll = None):
		if poll and self.isEnabledToAddPoll:
			instance , created = PollQuestionnaireAssigment.objects.get_or_create(poll = self , questionnaire = poll.getPollName)
			
	def removePoll(self , poll = None):
		if poll and self.isEnabledToRemovePoll:
			p = PollQuestionnaireAssigment.objects.filter(id = poll).first()
			if p:
				p.delete()
		
class PollQuestionnaireAssigment(models.Model):
	poll = models.ForeignKey(Poll , related_name="questionnaire")
	questionnaire = models.CharField(max_length = 250 , blank = True , null = True)
	completionTime = models.DurationField(null = True)
	restrictedMembers = models.ManyToManyField(ProxyUser , related_name="RestrictedQuestionnaires")
	exclusiveMembers = models.ManyToManyField(ProxyUser , related_name="ExclusiveQuestionnaires")
	requirements = models.ManyToManyField('PollQuestionnaireAssigment' , related_name="RequiredTo")
	
	def getMemberProgressURL(self, member = None):
		from r3s_cms.apps.system.templatetags.polls_tags import questionnaireViewUrl
		return questionnaireViewUrl(member = member , poll = self.poll , questionnaire = self)

	def getSuperviserMemberProgressURL(self, member = None):
		from r3s_cms.apps.system.templatetags.polls_tags import questionnaireSupervisedViewUrl
		return questionnaireSupervisedViewUrl(member = member , poll = self.poll , questionnaire = self)

	def _slug(self):
		if self.questionnaire:
			return self.questionnaire
		return None
	slug = property(_slug)
	
	def _isStartEnabled(self):
		if self.poll:
			return self.poll.isStartEnabled
		return False
	isStartEnabled = property(_isStartEnabled)
	
	def _start(self):
		if self.isStartEnabled:
			members = self.getMembers
			for member in members:
				self.createPoll(member = member)
	start=property(_start)
	
	def createPoll(self , member = None):
##		if self.isStartEnabled and member:
		if member:
			poll = self.getPoll
			if poll:
				poll.createPoll(poll = self.poll , assigment = self , member = member)
	
	def _getMembers(self):
		if self.exclusiveMembers.all().count() > 0:
			return self.exclusiveMembers.all()
		if self.poll:
			members = self.poll.getMembers
			if self.restrictedMembers.all().count() > 0:
				members = members.exclude(id__in = [m.id for m in self.restrictedMembers.all()])
			return members
		return ProxyUser.objects.none()
	getMembers = property(_getMembers)
	
	def _staffRemoveURL(self):
		return reverse('system_polls_staff_remove_poll' , kwargs={'poll': self.poll.id , 'questionnaire': self.id})
	staffRemoveURL = property(_staffRemoveURL)
	
	def _name(self):
		polls = self.poll.getPolls
		poll = polls.filter(model__iexact = self.questionnaire).first()
		if poll:
			name = poll.getName
		else:
			name = "Sin Nombre"
		return name
	name = property(_name)

	def _sectionName(self):
		polls = self.poll.getPolls
		poll = polls.filter(model__iexact = self.questionnaire).first()
		if poll:
			name = poll.getSectionName
		else:
			name = "Sin Nombre"
		return name
	sectionName = property(_sectionName)
	
	def _title(self):
		return self.name
	title = property(_title)
	
	def _subtitle(self):
		return "%s" % (self.sectionName)
	subtitle = property(_subtitle)

	def _getPoll(self):
		polls = self.poll.getPolls
		poll = polls.filter(model__iexact = self.questionnaire).first()
		return poll
	getPoll = property(_getPoll)
	
	def getMemberPoll(self , member = None):
		poll = self.getPoll
		memberPoll = None
		if member and poll:
			memberPoll = poll.getMemberPoll(poll = self.poll , member = member)
		return memberPoll

	def _getSortIndex(self):
		poll = self.getPoll
		if poll:
			return poll.getSortIndex
		return 0
	getSortIndex=property(_getSortIndex)

	def getProgress(self , member = None):
		if member:
			poll = self.getPoll
			if poll:
				return poll.getProgress(poll = self.poll , member = member)
		return 0
		
	def _questionNumber(self):
		poll = self.getPoll
		if poll:
			return poll.questionNumber
		return 0
	questionNumber = property(_questionNumber)
	
	def _template(self):
		poll = self.getPoll
		if poll:
			return poll.template
		return None
	template = property(_template)

class Base(models.Model):
##############CHARFIELD
	name = models.CharField(max_length = 250 , blank = True , null = True)
	section_name = models.CharField(max_length = 250 , blank = True , null = True)
##############INTEGER
	section_index = models.IntegerField(default = 0 , blank = True , null = True)
	index = models.IntegerField(default = 0 , blank = True , null = True)
##############TEXT
	header = models.TextField(blank = True , null = True)
##############FOREING KEY
	user = models.ForeignKey(ProxyUser , related_name="%(app_label)s_%(class)s_polls")
	poll = models.ForeignKey('Poll' , related_name="%(app_label)s_%(class)s_pollAssignments")
	assigment = models.ForeignKey('PollQuestionnaireAssigment' , related_name="%(app_label)s_%(class)s_assignments")
##############TIMESTAMPS
	assigned_timestamp = models.DateTimeField(auto_now_add = True , null = True)
	available_timestamp = models.DateTimeField(null = True)
	started_timestamp = models.DateTimeField(null = True)
	lastview_timestamp = models.DateTimeField(null = True)
	updated_timestamp = models.DateTimeField(null = True)
	commited_timestamp = models.DateTimeField(null = True)
	deadline_timestamp = models.DateTimeField(null = True)
##############FLAGS
	is_active = models.NullBooleanField(default = True)
	is_available = models.NullBooleanField(default = False)
	is_commited = models.NullBooleanField(default = False)
	is_started = models.NullBooleanField(default = False)
##############MANAGMENT
	objects = BaseActiveManager()
	commited = BaseCommitedManager()
	available = BaseAvailableManager()
	started = BaseStartedManager()

	class Meta:
		abstract = True

	def __unicode__(self):
		return self.__str__()

	def __str__(self):
		return "%s - %s - %s" %(self.__class__.getPollName() , self.poll , self.user)
		
	def _view(self):
		if self.isActive:
			if self.isAvailable:
				if not self.isCommited and not self.isStarted:
					self.setStarted
					self.setLastViewTimestamp(now = True)
				elif self.isStarted:
					self.setLastViewTimestamp(now = True)					
	view = property(_view)
	
	def _viewURL(self):
		return reverse('system_polls_my_polls_questionnaire_response_submit' , kwargs={'poll': self.poll.id , 'questionnaire': self.assigment.slug})
	viewURL = property(_viewURL)
	
	def _saveURL(self):
		return reverse('system_polls_my_polls_questionnaire_response_submit' , kwargs={'poll': self.poll.id , 'questionnaire': self.assigment.slug})
	saveURL = property(_saveURL)

	def _commitURL(self):
		return reverse('system_polls_my_polls_questionnaire_response_submit' , kwargs={'poll': self.poll.id , 'questionnaire': self.assigment.slug})
	commitURL = property(_commitURL)

	@classmethod
	def createPoll(cls , poll = None , assigment = None , member = None):
		instance = None
		if poll and assigment and member:
			instance , created = cls.objects.get_or_create(poll = poll , assigment = assigment , user = member , is_active = True , is_available = False , is_commited = False , is_started = False)
			print "instance: %s - created: %s" % (instance.id , created)
			if created:
				instance.setAvailable
		return instance

	def template(cls):
		return None
		
	def _formClass(self):
		return None
	formClass = property(_formClass)

	def _getProgress(self):
		totalAnswers = self.totalAnswers
		totalAnswered = self.totalAnswered
		progress = (totalAnswered * 100) / totalAnswers
		return progress
	getProgress = property(_getProgress)
	
	def _totalAnswers(self):
		return self.__class__.getTotalQuestions()
	totalAnswers = property(_totalAnswers)

	def _totalAnswered(self):
		return 0
	totalAnswered = property(_totalAnswered)
	
#	def totalAnswers(cls):
#		return 1

	def _index(self):
		return self.__class__.getPollIndex() or 0
	getIndex = property(_index)

	def _sectionIndex(self):
		return self.__class__.getPollSectionIndex() or 0
	getSectionIndex = property(_sectionIndex)

	def _name(self):
		return self.__class__.getPollName() or 'Sin Nombre'
	getName = property(_name)

	def _sectionName(self):
		return self.__class__.getPollSectionName() or 'Sin Nombre'
	getSectionName = property(_sectionName)

	@classmethod
	def getTotalQuestions(cls):
		return 1

	@classmethod
	def getSortIndex(cls):
		index = cls.getPollSectionIndex() * 1000
		index += cls.getPollIndex()
		return index

	@classmethod
	def getPollIndex(cls):
		return 0

	@classmethod
	def getPollSectionIndex(cls):
		return 0

	@classmethod
	def getPollName(cls):
		return ''

	@classmethod
	def getPollSectionName(cls):
		return ''

	@classmethod
	def assign(cls , user = None , poll = None):
		instance = None
		created = False
		if user and poll:
			instance , created = cls.objects.get_or_create(user = user , poll = poll , is_active = True)
		return instance , created

	@classmethod
	def hasHeader(cls):
		return False
	@classmethod
	def getHeader(cls):
		return None

	def _isSaveEnabled(self):
		if self.isActive and self.isStarted and self.isAvailable and not self.isCommited:
			return True
		return False
	isSaveEnabled = property(_isSaveEnabled)

	def _isCommitEnabled(self):
		if self.isSaveEnabled:
			return True
		return False
	isCommitEnabled = property(_isCommitEnabled)

	def _canBeSaved(self):
		return self.isSaveEnabled
	canBeSaved = property(_canBeSaved)

	def _canBeCommitted(self):
		return self.isSaveEnabled and self.readyToCommit
	canBeCommitted = property(_canBeCommitted)
	
	def _readyToCommit(self):
		return False
	readyToCommit = property(_readyToCommit)

	def _isActive(self):
		return self.is_active or False
	isActive = property(_isActive)

	def _isAvailable(self):
		return self.is_available or False
	isAvailable = property(_isAvailable)

	def _isCommited(self):
		return self.is_commited or False
	isCommited = property(_isCommited)

	def _isStarted(self):
		return self.is_started or False
	isStarted = property(_isStarted)

	def _setActive(self):
		if not self.isActive:
			self.is_active = True
			self.is_available = False
			self.is_commited = False
			self.is_started = False
			self.save()
			self.setAssignedTimestamp(now = True)
			self.setAvailableTimestamp(reset = True)
			self.setStartedTimestamp(reset = True)
			self.setLastViewTimestamp(reset = True)
			self.setUpdatedTimestamp(reset = True)
			self.setCommitedTimestamp(reset = True)
			self.setDeadlineTimestamp(reset = True)
	setActive = property(_setActive)

	def _setDeactive(self):
		self.is_active = False
		self.is_available = False
		self.is_commited = False
		self.is_started = False
		self.save()
		self.setAssignedTimestamp(reset = True)
		self.setAvailableTimestamp(reset = True)
		self.setStartedTimestamp(reset = True)
		self.setLastViewTimestamp(reset = True)
		self.setUpdatedTimestamp(reset = True)
		self.setCommitedTimestamp(reset = True)
		self.setDeadlineTimestamp(reset = True)
		self.clearData
	setDeactive = property(_setDeactive)

	def _setAvailable(self):
		if self.isActive:
			self.is_available = True
			self.is_commited = False
			self.is_started = False
			self.save()
			self.setAvailableTimestamp(now = True)
			self.setStartedTimestamp(reset = True)
			self.setLastViewTimestamp(reset = True)
			self.setUpdatedTimestamp(reset = True)
			self.setCommitedTimestamp(reset = True)
			self.setDeadlineTimestamp(reset = True)
	setAvailable = property(_setAvailable)
	
	def _setStarted(self):
		if self.isAvailable and not self.isStarted:
			self.is_commited = False
			self.is_started = True
			self.save()
			self.setStartedTimestamp(now = True)
			self.setLastViewTimestamp(reset = True)
			self.setUpdatedTimestamp(reset = True)
			self.setCommitedTimestamp(reset = True)
	setStarted = property(_setStarted)
	
	def _setCommited(self):
		if self.isStarted and not self.isCommited:
			self.is_commited = True
			self.save()
			self.setCommitedTimestamp(now = True)
	setCommited = property(_setCommited)
	
	def setDeadLine(self , time = None):
		if time:
			self.setDeadlineTimestamp(time = time)
	
	def _updated(self):
		self.setUpdatedTimestamp(now = True)
	updated = property(_updated)
	
	def setAssignedTimestamp(self , time = None , now = False , reset = False):
		if reset:
			self.assigned_timestamp = None
		elif now:
			self.assigned_timestamp = datetime.now()
		elif time:
			self.assigned_timestamp = None
		self.save()
	
	def setAvailableTimestamp(self , time = None , now = False , reset = False):
		if reset:
			self.available_timestamp = None
		elif now:
			self.available_timestamp = datetime.now()
		elif time:
			self.available_timestamp = None
		self.save()

	def setStartedTimestamp(self , time = None , now = False , reset = False):
		if reset:
			self.started_timestamp = None
		elif now:
			self.started_timestamp = datetime.now()
		elif time:
			self.started_timestamp = time
		self.save()

	def setLastViewTimestamp(self , time = None , now = False , reset = False):
		if reset:
			self.lastview_timestamp = None
		elif now:
			self.lastview_timestamp = datetime.now()
		elif time:
			self.lastview_timestamp = time
		self.save()

	def setUpdatedTimestamp(self , time = None , now = False , reset = False):
		if reset:
			self.updated_timestamp = None
		elif now:
			self.updated_timestamp = datetime.now()
		elif time:
			self.updated_timestamp = time
		self.save()

	def setCommitedTimestamp(self , time = None , now = False , reset = False):
		if reset:
			self.commited_timestamp = None
		elif now:
			self.commited_timestamp = datetime.now()
		elif time:
			self.commited_timestamp = time
		self.save()

	def setDeadlineTimestamp(self , time = None , now = False , reset = False):
		if reset:
			self.deadline_timestamp = None
		elif now:
			self.deadline_timestamp = datetime.now()
		elif time:
			self.deadline_timestamp = time
		self.save()
		
	def _clearData(self):
		pass
	clearData = property(_clearData)
########################################################################################################################
########################################################################################################################
#################################[-------------ENCUENSTAS-------------]#################################################
########################################################################################################################
########################################################################################################################
#################################[-------Inventario Talento-----------]#################################################
class IT_Talento(models.Model):
	name = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Nombre")
	position = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Puesto")
	years = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Años")
	months = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Meses")

class InventarioTalento(Base):
	talento = models.ManyToManyField(IT_Talento)
	generalComments = models.TextField(blank = True , null = True , verbose_name = "Comentarios Generales")

	def _formClass(self):
		from forms import InventarioTalentoForm
		return InventarioTalentoForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-I/inventario-talento/base.html'

	@classmethod
	def getPollIndex(cls):
		return 1

	@classmethod
	def getPollSectionIndex(cls):
		return 1

	@classmethod
	def getPollName(cls):
		return '1. Inventario de Talento'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase I - Análisis de la Situación Actual'

	def save(self, *args, **kwargs):
		self.name = '1. Inventario de Talento'
		self.section_name = 'Fase I - Análisis de la Situación Actual'
		self.section_index = 1
		self.index = 1
		super(InventarioTalento, self).save(*args, **kwargs)

	def addTalento(self , name = None , position = None , years = None , months = None):
		added = False
		if name and position and years and months:
			instance = IT_Talento.objects.create(name = name , position = position , years = years , months = months)
			if instance:
				self.talento.add(instance)
				self.save()
				self.setUpdatedTimestamp(now = True)
				added = True
		return added

	def removeTalento(self , id = None):
		removed = False
		if id:
			instance = self.talento.all().filter(id = id).first()
			if instance:
				self.talento.remove(instance)
				self.save()
				instance.delete()
				self.setUpdatedTimestamp(now = True)
				removed = True
		return removed
	
	@classmethod
	def hasHeader(cls):
		return False
	@classmethod
	def getHeader(cls):
		return None

#	def _totalAnswers(self):
#		return self.__class__.getTotalQuestions()
#	totalAnswers = property(_totalAnswers)

	@classmethod
	def getTotalQuestions(cls):
		return 2
	
	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	def _getTalentos(self):
		return self.talento.all()
	getTalentos=property(_getTalentos)
	
	def _talentosCount(self):
		return self.getTalentos.count()
	talentosCount=property(_talentosCount)

	def _question_1_answered(self):
		if self.talentosCount > 0:
			return True
		return False
	question_1_answered=property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "1. Inventario de Talento"

	def _question_1_has_header(self):
		return False
	question_1_has_header=property(_question_1_has_header)

	def question_1_header(cls):
		return None
	@classmethod
	def question_1_id(cls):
		return 'talento_id'

	def _question_2_answered(self):
		if self.generalComments and self.generalComments.strip():
			return True
		return False
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "Comentarios Generales"
	@classmethod
	def question_2_has_header(cls):
		return False
	@classmethod
	def question_2_header(cls):
		return None
	@classmethod
	def question_2_id(cls):
		return 'generalComments_id'
#################################[-------Mapeo Situacional-----------]#################################################
class MapeoSituacional(Base):
	question_1 = models.TextField(blank = True , null = True , verbose_name = "Dirige y Entrena" , help_text = 'Estrechamente cercano al colaborador, dando instrucciones claras y precisas, con un seguimiento muy frecuente.')
	question_2 = models.TextField(blank = True , null = True , verbose_name = "Orienta y Acompaña" , help_text = 'Explica las razones de las acciones y las tareas, considera necesario que el colaborar entienda las estrategias de las decisiones.')
	question_3 = models.TextField(blank = True , null = True , verbose_name = "Apoya y Escucha" , help_text = 'Estimula la creatividad y confía en que su colaborador cuenta con el potencial necesario para resolver situaciones complejas.')
	question_4 = models.TextField(blank = True , null = True , verbose_name = "Delega y Reconoce" , help_text = 'Asume que su colaborador tiene la capacidad para tomar decisiones adecuadas, motivando y apoyando la toma de riesgos.')
	generalComments = models.TextField(blank = True , null = True , verbose_name = "Comentarios Generales")

	def _formClass(self):
		from forms import MapeoSituacionalForm
		return MapeoSituacionalForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-I/mapeo-situacional/base.html'

	@classmethod
	def getPollIndex(cls):
		return 2

	@classmethod
	def getPollSectionIndex(cls):
		return 1

	@classmethod
	def getPollName(cls):
		return '2. Mapeo Situacional'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase I - Análisis de la Situación Actual'

	def save(self, *args, **kwargs):
		self.name = '2. Mapeo Situacional'
		self.section_name = 'Fase I - Análisis de la Situación Actual'
		self.section_index = 1
		self.index = 2
		super(MapeoSituacional, self).save(*args, **kwargs)
		
	@classmethod
	def hasHeader(cls):
		return True
	@classmethod
	def getHeader(cls):
		header = "<p>Llena el siguiente formulario de acuerdo con la teoria del liderazgo situacional, anota el nombre de cada uno de tus colaboradores en el cuadro que corresponda. Toma en cuenta el enfoque de cada uno de los cuadrantes:</p>"
		header += "<ol>"
		header += "<li>Alta orientación a las instrucciones y baja orientación a la motivación (colaborador nuevo en la empresa o nuevos en el puesto).</li>"
		header += "<li>Alta orientación a las instrucciones y alta orientación a la motivación (colaborador con un buen nivel de conocimiento de sus responsabilidades).</li>"
		header += "<li>Baja orientación a las instrucciones y alta orientación a la motivación (colaborador con alto conocimiento de sus responsabilidades y baja motivación).</li>"
		header += "<li>Baja orientación a las instrucciones y baja orientación a la motivación (colaborador altamente motivado y apto para la delegación).</li>"
		header += "</ol>"
		return header

	@classmethod
	def getTotalQuestions(cls):
		return 5

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		if self.question_3_answered:
			total += 1
		if self.question_4_answered:
			total += 1
		if self.question_5_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	def _question_1_answered(self):
		if self.question_1 and self.question_1.strip():
			return True
		return False
	question_1_answered = property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "1. Dirige y Entrena"
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "Estrechamente cernano al colaborador, dando instrucciones claras y precisas, con un seguimiento muy frecuente."
		return header
	@classmethod
	def question_1_id(cls):
		return 'question_1'

	def _question_1_value(self):
		return self.question_1 or ''
	question_1_value = property(_question_1_value)

	def _question_2_answered(self):
		if self.question_2 and self.question_2.strip():
			return True
		return False
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "2. Orienta y Acompaña"
	@classmethod
	def question_2_has_header(cls):
		return True
	@classmethod
	def question_2_header(cls):
		header = "Explica las razones de las acciones y las tareas, considera necesario que el colaborador entienda las estrategias de las decisiones."
		return header
	@classmethod
	def question_2_id(cls):
		return 'question_2'

	def _question_2_value(self):
		return self.question_2 or ''
	question_2_value = property(_question_2_value)

	def _question_3_answered(self):
		if self.question_3 and self.question_3.strip():
			return True
		return False
	question_3_answered = property(_question_3_answered)
	@classmethod
	def question_3_title(cls):
		return "3. Apoya y Escucha"
	@classmethod
	def question_3_has_header(cls):
		return True
	@classmethod
	def question_3_header(cls):
		header = "Estimula la creatividadd y confia en que su colaborador cuenta con el potencial necesario para resolver situaciones complejas."
		return header
	@classmethod
	def question_3_id(cls):
		return 'question_3'

	def _question_3_value(self):
		return self.question_3 or ''
	question_3_value = property(_question_3_value)

	def _question_4_answered(self):
		if self.question_4 and self.question_4.strip():
			return True
		return False
	question_4_answered = property(_question_4_answered)
	@classmethod
	def question_4_title(cls):
		return "4. Delega y Reconoce"
	@classmethod
	def question_4_has_header(cls):
		return True
	@classmethod
	def question_4_header(cls):
		header = "Asume que su colaborador tiene la capacidad para tomar decisiones adecuadas, motivando y apoyando la toma de riesgos."
		return header
	@classmethod
	def question_4_id(cls):
		return 'question_4'

	def _question_4_value(self):
		return self.question_4 or ''
	question_4_value = property(_question_4_value)

	def _question_5_answered(self):
		if self.generalComments and self.generalComments.strip():
			return True
		return False
	question_5_answered = property(_question_5_answered)
	@classmethod
	def question_5_title(cls):
		return "Comentarios Generales"
	@classmethod
	def question_5_has_header(cls):
		return False
	@classmethod
	def question_5_header(cls):
		header = None
		return header
	@classmethod
	def question_5_id(cls):
		return 'generalComments'

	def _question_5_value(self):
		return self.generalComments or ''
	question_5_value = property(_question_5_value)
#################################[-------Analisis Desempeño-----------]#################################################
class AD_EvaluacionIndividualColaboradores(models.Model):
	name = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Nombre")
	performance = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Nivel de Desempeño")
	actitute = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Actitudes y Conductas favorables")
class AD_SeleccionCoachee(models.Model):
	name = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Nombre")
	performance = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Desempeño")
	actitute = models.CharField(max_length = 250 , blank = True , null = True , verbose_name = "Actitud")
	
	def _isPerformance(self):
		if self.performance and self.performance.strip() and self.performance.upper() == 'TRUE':
			return True
		return False
	isPerformance = property(_isPerformance)
	
	def _isActitute(self):
		if self.actitute and self.actitute.strip() and self.actitute.upper() == 'TRUE':
			return True
		return False
	isActitute = property(_isActitute)
class AnalisisDesempegno(Base):
	talento = models.ManyToManyField(AD_EvaluacionIndividualColaboradores)
	coacheeSelection = models.ManyToManyField(AD_SeleccionCoachee)
	generalComments = models.TextField(blank = True , null = True , verbose_name = "Comentarios Generales")

	def _formClass(self):
		from forms import AnalisisDesempegnoForm
		return AnalisisDesempegnoForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-I/analisis-desempegno/base.html'

	@classmethod
	def getPollIndex(cls):
		return 3

	@classmethod
	def getPollSectionIndex(cls):
		return 1

	@classmethod
	def getPollName(cls):
		return '3. Análisis del Desempeño'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase I - Análisis de la Situación Actual'

	def save(self, *args, **kwargs):
		self.name = '3. Análisis del Desempeño'
		self.section_name = 'Fase I - Análisis de la Situación Actual'
		self.section_index = 1
		self.index = 3
		super(AnalisisDesempegno, self).save(*args, **kwargs)

	@classmethod
	def getTotalQuestions(cls):
		return 3

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		if self.question_3_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	def addTalento(self , name = None , performance = None , actitute = None):
		added = False
		if name and name.strip() and performance and performance.strip() and actitute and actitute.strip():
			instance = AD_EvaluacionIndividualColaboradores.objects.create(name = name , performance = performance , actitute = actitute)
			if instance:
				self.talento.add(instance)
				self.save()
				self.setUpdatedTimestamp(now = True)
				added = True
		return added
		
	def removeTalento(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.talentos.filter(id = id).first()
			if instance:
				self.talento.remove(instance)
				self.save()
				instance.delete()
				self.setUpdatedTimestamp(now = True)
				removed = True
		return removed

	def addCocheeSelection(self , name = None , performance = False , actitute = False):
		added = False
		if name and name.strip():
			print "%s - %s - %s" % (name , performance , actitute)
			instance = AD_SeleccionCoachee.objects.create(name = name , performance = performance , actitute = actitute)
			if instance:
				self.coacheeSelection.add(instance)
				self.save()
				self.setUpdatedTimestamp(now = True)
				added = True
		return added

	def removeCocheeSelection(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.coacheeSelection.filter(id = id).first()
			if instance:
				self.coacheeSelection.remove(instance)
				self.save()
				instance.delete()
				self.setUpdatedTimestamp(now = True)
				removed = True
		return removed

	def _talentos(self):
		return self.talento.all()
	talentos = property(_talentos)
	
	def _talentosCount(self):
		return self.talentos.count()
	talentosCount = property(_talentosCount)

	def _question_1_answered(self):
		return self.talentosCount > 0
	question_1_answered = property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "a) Evaluación individual de colaboradores"
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "De acuerdo a los resultados y comportamientos, establece el nivel de desempeño de cada uno de tus colaboradores."
		return header
	@classmethod
	def question_1_id(cls):
		return 'talento_id'
	@classmethod
	def question_1_value(cls):
		return []

	def _coacheeSelections(self):
		return self.coacheeSelection.all()
	coacheeSelections = property(_coacheeSelections)

	def _coacheeSelectionsCount(self):
		return self.coacheeSelections.count()
	coacheeSelectionsCount = property(_coacheeSelectionsCount)

	def _question_2_answered(self):
		return self.coacheeSelectionsCount > 0
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "b) Selección del Coachee"
	@classmethod
	def question_2_has_header(cls):
		return True
	@classmethod
	def question_2_header(cls):
		header = "Una vez realizada la evaluación de tus colaboradores, define los 4 colaboradores con los cuales desarrollaras procesos de coaching en acción."
		return header
	@classmethod
	def question_2_id(cls):
		return 'coacheeSelection_id'
	@classmethod
	def question_2_value(cls):
		return []

	def _question_3_answered(self):
		if self.generalComments and self.generalComments.strip():
			return True
		return False
	question_3_answered = property(_question_3_answered)
	@classmethod
	def question_3_title(cls):
		return "Comentarios Generales"
	@classmethod
	def question_3_has_header(cls):
		return False
	@classmethod
	def question_3_header(cls):
		header = None
		return header
	@classmethod
	def question_3_id(cls):
		return 'generalComments'

	def question_3_value(self):
		return self.generalComments or ''
#################################[-------Pre-Coaching-----------]#################################################
class PreCoaching(Base):
	target = models.TextField(blank = True , null = True , verbose_name = "Meta de Proceso de Coaching" , help_text = "De acuerdo a la situación actual de tu colaborador, el análisis situacional y a la evaluación del desempeño, establece la meta que quieres lograrr por lo cual iniciarás una proceso de Coaching")
	stronghold_1 = models.TextField(blank = True , null = True , verbose_name = "Fortaleza 1")
	stronghold_2 = models.TextField(blank = True , null = True , verbose_name = "Fortaleza 2")
	stronghold_3 = models.TextField(blank = True , null = True , verbose_name = "Fortaleza 3")
	opportunity_1 = models.TextField(blank = True , null = True , verbose_name = "Área de Oportunidad 1")
	opportunity_2 = models.TextField(blank = True , null = True , verbose_name = "Área de Oportunidad 2")
	opportunity_3 = models.TextField(blank = True , null = True , verbose_name = "Área de Oportunidad 3")
	recommendation_1 = models.TextField(blank = True , null = True , verbose_name = "Alternativa o Recomendación 1")
	recommendation_2 = models.TextField(blank = True , null = True , verbose_name = "Alternativa o Recomendación 2")
	recommendation_3 = models.TextField(blank = True , null = True , verbose_name = "Alternativa o Recomendación 3")
	session_1 = models.DateField(verbose_name = "Fecha de Primera Sesión" , blank = True , null = True)
	session_2 = models.DateField(verbose_name = "Fecha de Segunda Sesión" , blank = True , null = True)
	session_3 = models.DateField(verbose_name = "Fecha de Tercer Sesión" , blank = True , null = True)
	session_4 = models.DateField(verbose_name = "Fecha de Cuarta Sesión" , blank = True , null = True)
	session_5 = models.DateField(verbose_name = "Fecha de Quinta Sesión" , blank = True , null = True)
	session_6 = models.DateField(verbose_name = "Fecha de Sexta Sesión" , blank = True , null = True)
	place = models.TextField(blank = True , null = True , verbose_name = "Lugar en donde llevaras a cabo las sesiones de Coaching")	
	time = models.TextField(blank = True , null = True , verbose_name = "Horario en los cuales llevaras a cabo las sesiones de Coaching")	
	generalComments = models.TextField(blank = True , null = True , verbose_name = "Comentarios Generales de la sesión")

	def _formClass(self):
		from forms import PreCoachingForm
		return PreCoachingForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-II/pre-coaching/base.html'

	@classmethod
	def getTotalQuestions(cls):
		return 6

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		if self.question_3_answered:
			total += 1
		if self.question_4_answered:
			total += 1
		if self.question_5_answered:
			total += 1
		if self.question_6_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	@classmethod
	def getPollIndex(cls):
		return 1

	@classmethod
	def getPollSectionIndex(cls):
		return 2

	@classmethod
	def getPollName(cls):
		return 'Pre-coaching'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase II - Pre-Coaching'

	def save(self, *args, **kwargs):
		self.name = 'Pre-coaching'
		self.section_name = 'Fase II - Pre-Coaching'
		self.section_index = 2
		self.index = 1
		super(PreCoaching, self).save(*args, **kwargs)

	def _question_1_answered(self):
		if self.target and self.target.strip():
			return True
		return False
	question_1_answered = property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "1.- Meta de Proceso de Coaching."
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "De acuerdo a la situación actual de tu colaborador, el análisis situacional y a la evaluación del desempeño, estable la meta que quieres lograr por lo cual iniciarás un proceso de Coaching."
		return header
	@classmethod
	def question_1_id(cls):
		return 'target'

	def _question_1_value(self):
		return self.target or ''
	question_1_value = property(_question_1_value)

	def _question_2_answered(self):
		if self.stronghold_1 and self.stronghold_1.strip() and self.stronghold_2 and self.stronghold_2.strip() and self.stronghold_3 and self.stronghold_3.strip():
			return True
		return False
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "2.- Identificación de Fortalezas."
	@classmethod
	def question_2_has_header(cls):
		return True
	@classmethod
	def question_2_header(cls):
		header = "Describe las 3 fortalezas identificadas en tu colaborador, las cuales son claramente evidentes y observadas por ti durante tu experiencias como jefe."
		return header
	@classmethod
	def question_2a_label(cls):
		return 'Fortaleza 1'
	@classmethod
	def question_2a_id(cls):
		return 'stronghold_1'

	def _question_2a_value(self):
		return self.stronghold_1 or ''
	question_2a_value = property(_question_2a_value)
	@classmethod
	def question_2b_label(cls):
		return 'Fortaleza 2'
	@classmethod
	def question_2b_id(cls):
		return 'stronghold_2'

	def _question_2b_value(self):
		return self.stronghold_2 or ''
	question_2b_value = property(_question_2b_value)
	@classmethod
	def question_2c_label(cls):
		return 'Fortaleza 3'
	@classmethod
	def question_2c_id(cls):
		return 'stronghold_3'

	def _question_2c_value(self):
		return self.stronghold_3 or ''
	question_2c_value = property(_question_2c_value)

	def _question_3_answered(self):
		if self.opportunity_1 and self.opportunity_1.strip() and self.opportunity_2 and self.opportunity_2.strip() and self.opportunity_3 and self.opportunity_3.strip():
			return True
		return False
	question_3_answered = property(_question_3_answered)
	@classmethod
	def question_3_title(cls):
		return "3.- Áreas de oportunidad o mejora que hayas identificado."
	@classmethod
	def question_3_has_header(cls):
		return True
	@classmethod
	def question_3_header(cls):
		header = "Describe las 3 áreas de oportunidad identificadas en tu colaborador, las cuales son necesarias desarrollar para lograr un mejor desempeño y el logro de mejores resultados de acuerdo a sus responsabilidades directas del puesto que ocupa."
		return header
	@classmethod
	def question_3a_label(cls):
		return 'Área de Oportunidad 1'
	@classmethod
	def question_3a_id(cls):
		return 'opportunity_1'

	def _question_3a_value(self):
		return self.opportunity_1 or ''
	question_3a_value = property(_question_3a_value)
	@classmethod
	def question_3b_label(cls):
		return 'Área de Oportunidad 2'
	@classmethod
	def question_3b_id(cls):
		return 'opportunity_2'

	def _question_3b_value(self):
		return self.opportunity_2 or ''
	question_3b_value = property(_question_3b_value)
	@classmethod
	def question_3c_label(cls):
		return 'Área de Oportunidad 3'
	@classmethod
	def question_3c_id(cls):
		return 'opportunity_3'

	def _question_3c_value(self):
		return self.opportunity_3 or ''
	question_3c_value = property(_question_3c_value)

	def _question_4_answered(self):
		if self.recommendation_1 and self.recommendation_1.strip() and self.recommendation_2 and self.recommendation_2.strip() and self.recommendation_3 and self.recommendation_3.strip():
			return True
		return False
	question_4_answered = property(_question_4_answered)
	@classmethod
	def question_4_title(cls):
		return "4.- Alternativas o recomendaciones para la mejora."
	@classmethod
	def question_4_has_header(cls):
		return False
	@classmethod
	def question_4_header(cls):
		header = None
		return header
	@classmethod
	def question_4a_label(cls):
		return 'Alternativa o Recomendación 1'
	@classmethod
	def question_4a_id(cls):
		return 'recommendation_1'

	def _question_4a_value(self):
		return self.recommendation_1 or ''
	question_4a_value = property(_question_4a_value)
	@classmethod
	def question_4b_label(cls):
		return 'Alternativa o Recomendación 2'
	@classmethod
	def question_4b_id(cls):
		return 'recommendation_2'

	def _question_4b_value(self):
		return self.recommendation_2 or ''
	question_4b_value = property(_question_4b_value)
	@classmethod
	def question_4c_label(cls):
		return 'Alternativa o Recomendación 3'
	@classmethod
	def question_4c_id(cls):
		return 'recommendation_3'

	def _question_4c_value(self):
		return self.recommendation_3 or ''
	question_4c_value = property(_question_4c_value)

	def _question_5_answered(self):
		if self.session_1 and self.session_2 and self.session_3 and self.session_4 and self.session_5 and self.session_6 and self.place and self.place.strip() and self.time and self.time.strip():
			return True
		return False
	question_5_answered = property(_question_5_answered)
	@classmethod
	def question_5_title(cls):
		return "5.- Establecimiento de la Agenda de Coaching."
	@classmethod
	def question_5_has_header(cls):
		return True
	@classmethod
	def question_5_header(cls):
		header = "El Proceso de Coaching está compuesto por 6 sesiones, estable las fechas, horarios y lugares en los cuales harás tus sesiones de Coaching"
		return header
	@classmethod
	def question_5a_label(cls):
		return 'Fecha de Primera Sesión'
	@classmethod
	def question_5a_id(cls):
		return 'session_1'

	def _question_5a_value(self):
		return self.session_1 or ''
	question_5a_value = property(_question_5a_value)
	@classmethod
	def question_5b_label(cls):
		return 'Fecha de Segunda Sesión'
	@classmethod
	def question_5b_id(cls):
		return 'session_2'

	def _question_5b_value(self):
		return self.session_2 or ''
	question_5b_value = property(_question_5b_value)
	@classmethod
	def question_5c_label(cls):
		return 'Fecha de Tercer Sesión'
	@classmethod
	def question_5c_id(cls):
		return 'session_3'

	def _question_5c_value(self):
		return self.session_3 or ''
	question_5c_value = property(_question_5c_value)
	@classmethod
	def question_5d_label(cls):
		return 'Fecha de Cuarta Sesión'
	@classmethod
	def question_5d_id(cls):
		return 'session_4'

	def _question_5d_value(self):
		return self.session_4 or ''
	question_5d_value = property(_question_5d_value)
	@classmethod
	def question_5e_label(cls):
		return 'Fecha de Quinta Sesión'
	@classmethod
	def question_5e_id(cls):
		return 'session_5'

	def _question_5e_value(self):
		return self.session_5 or ''
	question_5e_value = property(_question_5e_value)
	@classmethod
	def question_5f_label(cls):
		return 'Fecha de Sexta Sesión'
	@classmethod
	def question_5f_id(cls):
		return 'session_6'

	def _question_5f_value(self):
		return self.session_6 or ''
	question_5f_value = property(_question_5f_value)
	@classmethod
	def question_5g_label(cls):
		return 'Lugar en donde llevaras a cabo las sesiones de Coaching'
	@classmethod
	def question_5g_id(cls):
		return 'place'

	def _question_5g_value(self):
		return self.place or ''
	question_5g_value = property(_question_5g_value)
	@classmethod
	def question_5h_label(cls):
		return 'Horarios en los cuales llevaras a cabo las sessiones de Coaching'
	@classmethod
	def question_5h_id(cls):
		return 'time'

	def _question_5h_value(self):
		return self.time or ''
	question_5h_value = property(_question_5h_value)

	def _question_6_answered(self):
		if self.generalComments and self.generalComments.strip():
			return True
		return False
	question_6_answered = property(_question_6_answered)
	@classmethod
	def question_6_title(cls):
		return "Comentarios Generales de la sesión."
	@classmethod
	def question_6_has_header(cls):
		return False
	@classmethod
	def question_6_header(cls):
		header = None
		return header
	@classmethod
	def question_6_id(cls):
		return 'generalComments'

	def _question_6_value(self):
		return self.generalComments or ''
	question_6_value = property(_question_6_value)
#################################[-------Sesion 1-----------]#################################################
class SO_RetroalimentacionInicial(models.Model):
	aspect = models.TextField(blank = True , null = True , verbose_name = "Aspecto")
	description = models.TextField(blank = True , null = True , verbose_name = "Describir")
	evidence = models.TextField(blank = True , null = True , verbose_name = "Evidencia/Ejemplo")
class SO_AreaOportunidad(models.Model):
	area = models.TextField(blank = True , null = True , verbose_name = "Área de Oportunidad")
	description = models.TextField(blank = True , null = True , verbose_name = "Describir")
	evidence = models.TextField(blank = True , null = True , verbose_name = "Evidencia/Ejemplo")
class SessionOne(Base):
	initial_feedback = models.ManyToManyField(SO_RetroalimentacionInicial)
	opportunities = models.ManyToManyField(SO_AreaOportunidad)
	expectation = models.TextField(blank = True , null = True , verbose_name = "Calibración de Expectativas" , help_text = "Define los argumentos que utilizarás para generar compromiso y motivación hacia la mejora y hacia el proceso de coaching que iniciaras.")
	comments = models.TextField(blank = True , null = True , verbose_name = "Comentarios del Colaborador")
	targets = models.TextField(blank = True , null = True , verbose_name = "Definición de Meta del Proceso" , help_text = "Describe la meta que establecerás con el colaborador, la cual será el enfoque y motivo del proceso de coaching.")

	def _formClass(self):
		from forms import SessionOneForm
		return SessionOneForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-III/sesion-1/base.html'

	@classmethod
	def getTotalQuestions(cls):
		return 5
		
	def addFeedback(self , aspect = None , description = None , evidence = None):
		added = False
		if aspect and aspect.strip() and description and description.strip() and evidence and evidence.strip():
			instance = SO_RetroalimentacionInicial.objects.create(aspect = aspect , description = description , evidence = None)
			if instance:
				self.initial_feedback.add(instance)
				self.save()
				self.setUpdatedTimestamp(now = True)
				added = True
		return added
		
	def removeFeedback(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.feedbacks.filter(id = id).first()
			if instance:
				self.initial_feedback.remove(instance)
				self.save()
				instance.delete()
				self.setUpdatedTimestamp(now = True)
				removed = True
		return removed

	def addOpportunity(self , area = None , description = None , evidence = None):
		added = False
		if area and area.strip() and description and description.strip() and evidence and evidence.strip():
			instance = SO_AreaOportunidad.objects.create(area = area , description = description , evidence = evidence)
			if instance:
				self.opportunities.add(instance)
				self.save()
				self.setUpdatedTimestamp(now = True)
				added = True
		return added

	def removeOpportunity(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.opportunitiess.filter(id = id).first()
			if instance:
				self.opportunities.remove(instance)
				self.save()
				instance.delete()
				self.setUpdatedTimestamp(now = True)
				removed = True
		return removed

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		if self.question_3_answered:
			total += 1
		if self.question_4_answered:
			total += 1
		if self.question_5_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	@classmethod
	def getPollIndex(cls):
		return 1

	@classmethod
	def getPollSectionIndex(cls):
		return 3

	@classmethod
	def getPollName(cls):
		return 'Sesión 1'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase III - Sesiones de Coaching'

	def save(self, *args, **kwargs):
		self.name = 'Sesión 1'
		self.section_name = 'Fase III - Sesiones de Coaching'
		self.section_index = 3
		self.index = 1
		super(SessionOne, self).save(*args, **kwargs)
	@classmethod
	def hasHeader(cls):
		return True
	@classmethod
	def getHeader(cls):
		header = "<p>"
		header += "1.- Retroalimentación Inicial"
		header += "</p>"
		header += "<p>"
		header += "El Proceso de Coaching inicia con una sesión de retroalimentación donde explicas al colaboraror, los motivos por los cuales decides iniciar un proceso de Coaching."
		header += "</p>"
		header += "<p>"
		header += "Identifica los aspectos que se te solicitarán."
		header += "</br>"
		header += "*Recuerda que una retroalimetnación debe ser objetiva, libre de prejuicios y evidente."
		header += "</p>"
		return header

	def _feedbacks(self):
		return self.initial_feedback.all()
	feedbacks = property(_feedbacks)

	def _feedbackCount(self):
		return self.feedbacks.count()
	feedbackCount = property(_feedbackCount)

	def _question_1_answered(self):
		return self.feedbackCount > 0
	question_1_answered = property(_question_1_answered)
	
	def _opportunitiess(self):
		return self.opportunities.all()
	opportunitiess = property(_opportunitiess)
	
	def _opportunitiessCount(self):
		return self.opportunitiess.count()
	opportunitiessCount = property(_opportunitiessCount)
	
	@classmethod
	def question_1_title(cls):
		return "a) Aspectos positivos del colaborador"
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "Define tres aspectos positivos, fortalezas o cualidades para retroalimentar."
		return header
	@classmethod
	def question_1_id(cls):
		return 'initial_feedback_id'
	@classmethod
	def question_1_value(cls):
		return []

	def _question_2_answered(self):
		return self.opportunitiessCount > 0
	question_2_answered = property(_question_2_answered)

	@classmethod
	def question_2_title(cls):
		return "b) Áreas de oportunidad"
	@classmethod
	def question_2_has_header(cls):
		return True
	@classmethod
	def question_2_header(cls):
		header = "Define tres aspectos que puedan ser mejorados para retroalimentar."
		return header
	@classmethod
	def question_2_id(cls):
		return 'opportunities_id'
	@classmethod
	def question_2_value(cls):
		return []

	def _question_3_answered(self):
		if self.expectation and self.expectation.strip():
			return True
		return False
	question_3_answered = property(_question_3_answered)
	@classmethod
	def question_3_title(cls):
		return "2.- Calibración de Expectativas"
	@classmethod
	def question_3_has_header(cls):
		return True
	@classmethod
	def question_3_header(cls):
		header = "Define los argumentos que utilizarás para generar compromiso y motivación hacia la mejora y hacia el proceo de coaching que iniciaras."
		return header
	@classmethod
	def question_3_id(cls):
		return 'expectation'

	def _question_3_value(self):
		return self.expectation or ''
	question_3_value = property(_question_3_value)

	def _question_4_answered(self):
		if self.comments and self.comments.strip():
			return True
		return False
	question_4_answered = property(_question_4_answered)
	@classmethod
	def question_4_title(cls):
		return "Comentarios del Colaborar"
	@classmethod
	def question_4_has_header(cls):
		return False
	@classmethod
	def question_4_header(cls):
		header = None
		return header
	@classmethod
	def question_4_id(cls):
		return 'comments'

	def _question_4_value(self):
		return self.comments or ''
	question_4_value = property(_question_4_value)

	def _question_5_answered(self):
		if self.targets and self.targets.strip():
			return True
		return False
	question_5_answered = property(_question_5_answered)
	@classmethod
	def question_5_title(cls):
		return "3.- Definición de Meta del Proceso"
	@classmethod
	def question_5_has_header(cls):
		return True
	@classmethod
	def question_5_header(cls):
		header = "Describe la meta que establecerás con el colaborador, la cual será el enfoque y motivo del proceso de coaching."
		return header
	@classmethod
	def question_5_id(cls):
		return 'targets'

	def _question_5_value(self):
		return self.targets or ''
	question_5_value = property(_question_5_value)
#################################[-------Sesion 2-----------]#################################################
class ST_improvementOne(models.Model):
	need = models.TextField(blank = True , null = True , verbose_name = "Necesidad")
	description = models.TextField(blank = True , null = True , verbose_name = "Describir")
class ST_improvementTwo(models.Model):
	resource = models.TextField(blank = True , null = True , verbose_name = "Recursos")
	habit = models.NullBooleanField(verbose_name = "Habitos")
	actitude = models.NullBooleanField(verbose_name = "Actitudes")
	learning = models.NullBooleanField(verbose_name = "Aprendizaje")
	description = models.TextField(blank = True , null = True , verbose_name = "Describir")
class ST_actionPlan(models.Model):
	skills = models.TextField(blank = True , null = True , verbose_name = "Habilidades")
	technique = models.NullBooleanField(verbose_name = "Técnicas")
	interpersonal = models.NullBooleanField(verbose_name = "Interpersonales")
#	learning = models.NullBooleanField(verbose_name = "Aprendizaje")
	description = models.TextField(blank = True , null = True , verbose_name = "Describir")
class SessionTwo(Base):
	improvementOne = models.ManyToManyField(ST_improvementOne)
	improvementTwo = models.ManyToManyField(ST_improvementTwo)
	actionPlan = models.ManyToManyField(ST_actionPlan)
	generalComments = models.TextField(blank = True , null = True , verbose_name = "Comentarios Generales")

	def _formClass(self):
		from forms import SessionTwoForm
		return SessionTwoForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-III/sesion-2/base.html'

	@classmethod
	def getTotalQuestions(cls):
		return 4

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		if self.question_3_answered:
			total += 1
		if self.question_4_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	def addImprovementOne(self , need = None , description = None):
		added = False
		if need and need.strip() and description and description.strip():
			instance = ST_improvementOne.objects.create(need = need , description = description)
			if instance:
				self.improvementOne.add(instance)
				added = True
				self.setUpdatedTimestamp(now = True)
		return added
		
	def removeImprovementOne(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.improvementsOne.filter(id = id).first()
			if instance:
				self.improvementOne.remove(instance)
				instance.delete()
				removed = True
				self.setUpdatedTimestamp(now = True)
		return removed

	def addImprovementTwo(self , resource = None , habit = None , actitude = None , learning = None , description = None):
		added = False
		if resource and resource.strip() and description and description.strip():
			instance = ST_improvementTwo.objects.create(resource = resource , habit = habit , actitude = actitude , learning = learning , description = description)
			if instance:
				self.improvementTwo.add(instance)
				added = True
				self.setUpdatedTimestamp(now = True)
		return added

	def removeImprovementTwo(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.improvementsTwo.filter(id = id).first()
			if instance:
				self.improvementTwo.remove(instance)
				instance.delete()
				removed = True
				self.setUpdatedTimestamp(now = True)
		return removed

	def addActionPlan(self , skills = None , technique = None , interpersonal = None , description = None):
		added = False
		if skills and skills.strip() and description and description.strip():
			instance = ST_actionPlan.objects.create(skills = skills , technique = technique , interpersonal = interpersonal , description = description)
			if instance:
				self.actionPlan.add(instance)
				added = True
				self.setUpdatedTimestamp(now = True)
		return added

	def removeActionPlan(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.actionsPlan.filter(id = id).first()
			if instance:
				self.actionPlan.remove(instance)
				instance.delete()
				removed = True
				self.setUpdatedTimestamp(now = True)
		return removed

	def _improvementsOne(self):
		return self.improvementOne.all()
	improvementsOne = property(_improvementsOne)

	def _improvementsOneCount(self):
		return self.improvementsOne.count()
	improvementsOneCount = property(_improvementsOneCount)

	def _improvementsTwo(self):
		return self.improvementTwo.all()
	improvementsTwo = property(_improvementsTwo)

	def _improvementsTwoCount(self):
		return self.improvementsTwo.count()
	improvementsTwoCount = property(_improvementsTwoCount)

	def _actionsPlan(self):
		return self.actionPlan.all()
	actionsPlan = property(_actionsPlan)

	def _actionsPlanCount(self):
		return self.actionsPlan.count()
	actionsPlanCount = property(_actionsPlanCount)

	@classmethod
	def getPollIndex(cls):
		return 2

	@classmethod
	def getPollSectionIndex(cls):
		return 3

	@classmethod
	def getPollName(cls):
		return 'Sesión 2'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase III - Sesiones de Coaching'

	def save(self, *args, **kwargs):
		self.name = 'Sesión 2'
		self.section_name = 'Fase III - Sesiones de Coaching'
		self.section_index = 3
		self.index = 2
		super(SessionTwo, self).save(*args, **kwargs)

	def _question_1_answered(self):
		return self.improvementsOneCount > 0
	question_1_answered = property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "1.- Identificación de necesidades de mejora"
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "Identifica junto con el colaborar las 3 necesidades clave que requiere mejorar para lograr la meta definida."
		return header
	@classmethod
	def question_1_id(cls):
		return 'improvementOne'
	@classmethod
	def question_1_value(cls):
		return []

	def _question_2_answered(self):
		return self.improvementsTwoCount > 0
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "2.- Identificación de necesidades de mejora"
	@classmethod
	def question_2_has_header(cls):
		return True
	@classmethod
	def question_2_header(cls):
		header = "Identifica junto con el colaborar los recursos necesarios que requiere para lograr la meta definida."
		return header
	@classmethod
	def question_2_id(cls):
		return 'improvementTwo'
	@classmethod
	def question_2_value(cls):
		return []

	def _question_3_answered(self):
		return self.actionsPlanCount > 0
	question_3_answered = property(_question_3_answered)
	@classmethod
	def question_3_title(cls):
		return "3.- Plan de Acción"
	@classmethod
	def question_3_has_header(cls):
		return False
	@classmethod
	def question_3_header(cls):
		header = None
		return header
	@classmethod
	def question_3_id(cls):
		return 'actionPlan'
	@classmethod
	def question_3_value(cls):
		return []

	def _question_4_answered(self):
		if self.generalComments and self.generalComments.strip():
			return True
		return False
	question_4_answered = property(_question_4_answered)
	@classmethod
	def question_4_title(cls):
		return "Comentarios Generales"
	@classmethod
	def question_4_has_header(cls):
		return False
	@classmethod
	def question_4_header(cls):
		header = None
		return header
	@classmethod
	def question_4_id(cls):
		return 'generalComments'

	def _question_4_value(self):
		return self.generalComments or ''
	question_4_value = property(_question_4_value)
#################################[-------Sesion 3-----------]#################################################
class ST_accion(models.Model):
	action = models.TextField(blank = True , null = True , verbose_name = "Acción")
	description = models.TextField(blank = True , null = True , verbose_name = "Describir")
	code = models.TextField(verbose_name = "Indicador Clave")
	expectedResult = models.TextField(verbose_name = "Resultado Esperado")
	startDate = models.DateField(verbose_name = "Fecha de Inicio" , blank = True , null = True)
	timing = models.FloatField(verbose_name = "Tiempo de Desarrollo (Meses)" , blank = True , null = True)
class SessionThree(Base):
	action = models.ManyToManyField(ST_accion)
	generalComments = models.TextField(blank = True , null = True , verbose_name = "Comentarios Generales")

	def _formClass(self):
		from forms import SessionThreeForm
		return SessionThreeForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-III/sesion-3/base.html'

	@classmethod
	def getTotalQuestions(cls):
		return 2

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	@classmethod
	def getPollIndex(cls):
		return 3

	@classmethod
	def getPollSectionIndex(cls):
		return 3

	@classmethod
	def getPollName(cls):
		return 'Sesión 3'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase III - Sesiones de Coaching'

	def save(self, *args, **kwargs):
		self.name = 'Sesión 3'
		self.section_name = 'Fase III - Sesiones de Coaching'
		self.section_index = 3
		self.index = 3
		super(SessionThree, self).save(*args, **kwargs)

	def addAction(self , action = None , description = None , code = None , expectedResult = None , startDate = None , timing = None):
		added = False
		if action and description and code and expectedResult and startDate and timing:
			instance = ST_accion.objects.create(action = action , description = description , code = code , expectedResult = expectedResult , startDate = startDate , timing = timing)
			if instance:
				self.action.add(instance)
				self.save()
				self.setUpdatedTimestamp(now = True)
				added = True
		return added
	
	def removeAction(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.actions.filter(id = id).first()
			if instance:
				self.action.remove(instance)
				self.save()
				removed = True
				instance.delete()
				self.setUpdatedTimestamp(now = True)
		return removed

	def _actions(self):
		return self.action.all()
	actions = property(_actions)
	
	def _actionsCount(self):
		return self.actions.count()
	actionsCount = property(_actionsCount)

	def _question_1_answered(self):
		return self.actionsCount > 0
	question_1_answered = property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "1.- Plan de acción"
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "Define junto con el colaborador el plan de acción necesario para el logro de la meta."
		return header
	@classmethod
	def question_1_id(cls):
		return 'action_id'
	@classmethod
	def question_1_value(cls):
		return []

	def _question_2_answered(self):
		if self.generalComments and self.generalComments.strip():
			return True
		return False
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "Comentarios Generales"
	@classmethod
	def question_2_has_header(cls):
		return False
	@classmethod
	def question_2_header(cls):
		header = None
		return header
	@classmethod
	def question_2_id(cls):
		return 'generalComments'

	def _question_2_value(self):
		return self.generalComments or ''
	question_2_value = property(_question_2_value)
#################################[-------Sesion 4-----------]#################################################
class sf_performance(models.Model):
	performance = models.TextField(blank = True , null = True , verbose_name = "Indicador clave de desempeño.")
	result = models.TextField(blank = True , null = True , verbose_name = "Resultado esperado.")
class SessionFour(Base):
	delegated_task = models.TextField(blank = True , null = True , verbose_name = "Describe la tarea que delegarás a tu colaborador." , help_text = "Asegúrate que la tarea pueda ser delegada sin poner en riesgo un procedimiento o protocolo establecido.")
	task_impact = models.TextField(blank = True , null = True , verbose_name = "Describe cómo es que esta tarea impacta positivamente al plan de acción.")
	first_instruction = models.TextField(blank = True , null = True , verbose_name = "primer elemento de instrucciones.")
	second_instruction = models.TextField(blank = True , null = True , verbose_name = "segundo elemento de instrucciones.")
	third_instruction = models.TextField(blank = True , null = True , verbose_name = "tercer elemento de instrucciones.")
	benefit = models.TextField(blank = True , null = True , verbose_name = "Define cuáles son los principales beneficios para tu colaborador al realziar ezta tarea.")
	next_task = models.TextField(blank = True , null = True , verbose_name = "Una vez concluida la tarea, cuál será la siguiente tarea que le delegarás?.")
	performance = models.ManyToManyField(sf_performance)
	comments = models.TextField(blank = True , null = True , verbose_name = "Comenta cuales fueron las evidencias que te confirmaron el compromiso de tu colaborador respecto a la tarea delegada.")

	def _formClass(self):
		from forms import SessionFourForm
		return SessionFourForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-III/sesion-4/base.html'

	@classmethod
	def getTotalQuestions(cls):
		return 7

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		if self.question_3_answered:
			total += 1
		if self.question_4_answered:
			total += 1
		if self.question_5_answered:
			total += 1
		if self.question_6_answered:
			total += 1
		if self.question_7_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	@classmethod
	def getPollIndex(cls):
		return 4

	@classmethod
	def getPollSectionIndex(cls):
		return 3

	@classmethod
	def getPollName(cls):
		return 'Sesión 4 - Delegación'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase III - Sesiones de Coaching'

	def save(self, *args, **kwargs):
		self.name = 'Sesión 4 - Delegación'
		self.section_name = 'Fase III - Sesiones de Coaching'
		self.section_index = 3
		self.index = 4
		super(SessionFour, self).save(*args, **kwargs)
	@classmethod
	def hasHeader(cls):
		return True
	@classmethod
	def getHeader(cls):
		header = "<p>De acuerdo al plan de acción definido con tu colaborador, establece una tarea que le ayude a lograr dicho plan y que le permita desarrollar una o varias habilidades requeridas para su mejora individual.</p>"
		header += "<p>Asegúrate de que la tarea cumpla con las 3 reglas de una buena asignación de tareas:</p>"
		header += "<ol>"
		header += "<li>que este ligada al plan de acción.</li>"
		header += "<li>que le permita un beneficio o desarrollo significativo.</li>"
		header += "<li>que este 100% en sus manos el poder ejecutarla.</li>"
		header += "</ol>"
		header += "<p>No olvides confirmar la claridad de la tarea y el compromiso.</p>"
		return header

	def _question_1_answered(self):
		return self.question_1_value and self.question_1_value.strip()
	question_1_answered = property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "1.- Describe la tarea que delegarás a tu colaborador."
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "Asegúrate que la tarea pueda ser delegada sin poner en riesgo un procedimiento o protocolo establecido."
		return header
	@classmethod
	def question_1_id(cls):
		return 'delegated_task'

	def _question_1_value(self):
		return self.delegated_task or ''
	question_1_value = property(_question_1_value)

	def _question_2_answered(self):
		return self.question_2_value and self.question_2_value.strip()
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "2.- Describe cómo es que esta tarea impacta positivamente al plan de acción."
	@classmethod
	def question_2_has_header(cls):
		return False
	@classmethod
	def question_2_header(cls):
		header = None
		return header
	@classmethod
	def question_2_id(cls):
		return 'task_impact'

	def _question_2_value(self):
		return self.task_impact or ''
	question_2_value = property(_question_2_value)

	def _question_3_answered(self):
		return self.question_3a_value and self.question_3a_value.strip() and self.question_3b_value and self.question_3b_value.strip() and self.question_3c_value and self.question_3c_value.strip()
	question_3_answered = property(_question_3_answered)
	@classmethod
	def question_3_title(cls):
		return "3.- Enlista los 3 elementos más relevantes que deberá contener tu explicación de instrucciones para tu colaborador."
	@classmethod
	def question_3_has_header(cls):
		return False
	@classmethod
	def question_3_header(cls):
		header = None
		return header
	@classmethod
	def question_3a_label(cls):
		return 'a) primer elemento de instrucciones.'
	@classmethod
	def question_3a_id(cls):
		return 'first_instruction'

	def _question_3a_value(self):
		return self.first_instruction or ''
	question_3a_value = property(_question_3a_value)
	@classmethod
	def question_3b_label(cls):
		return 'b) segundo elemento de instrucciones.'
	@classmethod
	def question_3b_id(cls):
		return 'second_instruction'

	def _question_3b_value(self):
		return self.second_instruction or ''
	question_3b_value = property(_question_3b_value)
	@classmethod
	def question_3c_label(cls):
		return 'c) tercer elemento de instrucciones.'
	@classmethod
	def question_3c_id(cls):
		return 'third_instruction'

	def _question_3c_value(self):
		return self.third_instruction or ''
	question_3c_value = property(_question_3c_value)

	def _question_4_answered(self):
		if self.benefit and self.benefit.split():
			return True
		return False
	question_4_answered = property(_question_4_answered)
	@classmethod
	def question_4_title(cls):
		return "4.- Define cuáles son los principales beneficios para tu colaborar al realizar esta tarea."
	@classmethod
	def question_4_has_header(cls):
		return False
	@classmethod
	def question_4_header(cls):
		header = None
		return header
	@classmethod
	def question_4_id(cls):
		return 'benefit'

	def _question_4_value(self):
		return self.benefit or ''
	question_4_value = property(_question_4_value)

	def _question_5_answered(self):
		if self.next_task and self.next_task.split():
			return True
		return False
	question_5_answered = property(_question_5_answered)
	@classmethod
	def question_5_title(cls):
		return "5.-Una vez concluida la tarea, cuál será la siguiente tarea que le delegarás?"
	@classmethod
	def question_5_has_header(cls):
		return False
	@classmethod
	def question_5_header(cls):
		header = None
		return header
	@classmethod
	def question_5_id(cls):
		return 'next_task'

	def _question_5_value(self):
		return self.next_task or ''
	question_5_value = property(_question_5_value)

	def _question_6_answered(self):
		return self.performancesCount > 0
	question_6_answered = property(_question_6_answered)
	
	def _performances(self):
		return self.performance.all()
	performances = property(_performances)
	
	def _performancesCount(self):
		return self.performances.count()
	performancesCount = property(_performancesCount)
	
	def addPerformance(self , performance = None , result = None):
		added = False
		if performance and performance.strip() and result and result.strip():
			instance = sf_performance.objects.create(performance = performance , result = result)
			if instance:
				self.performance.add(instance)
				self.save()
				added = True
				self.setUpdatedTimestamp(now = True)
		return added
		
	def removePerformance(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.performances.filter(id = id).first()
			if instance:
				self.performance.remove(instance)
				self.save()
				instance.delete()
				self.setUpdatedTimestamp(now = True)
				removed = True
		return removed
	
	@classmethod
	def question_6_title(cls):
		return "6.- Define los indicadores clave de desempeño que impactarán positivamente esta tarea y los resultados esperados."
	@classmethod
	def question_6_has_header(cls):
		return False
	@classmethod
	def question_6_header(cls):
		header = None
		return header
	@classmethod
	def question_6_id(cls):
		return 'performance_id'

	def _question_6_value(self):
		return ""
	question_6_value = property(_question_6_value)

	def _question_7_answered(self):
		if self.comments and self.comments.split():
			return True
		return False
	question_7_answered = property(_question_7_answered)
	@classmethod
	def question_7_title(cls):
		return "7.- Comenta cuales fueron las evidencias que te confirmaron el compromiso de tu colaborador respecto a la tarea delegada."
	@classmethod
	def question_7_has_header(cls):
		return False
	@classmethod
	def question_7_header(cls):
		header = None
		return header
	@classmethod
	def question_7_id(cls):
		return 'comments'

	def _question_7_value(self):
		return self.comments or ''
	question_7_value = property(_question_7_value)
#################################[-------Sesion 5-----------]#################################################
class SessionFive(Base):
	delegated_task = models.TextField(blank = True , null = True , verbose_name = "Describe la tarea que delegarás a tu colaborador." , help_text = "Asegúrate que la tarea pueda ser delegada sin poner en riesgo un procedimiento o protocolo establecido.")
	task_impact = models.TextField(blank = True , null = True , verbose_name = "Describe cómo es que esta tarea impacta positivamente al plan de acción.")
	first_instruction = models.TextField(blank = True , null = True , verbose_name = "primer elemento de instrucciones.")
	second_instruction = models.TextField(blank = True , null = True , verbose_name = "segundo elemento de instrucciones.")
	third_instruction = models.TextField(blank = True , null = True , verbose_name = "tercer elemento de instrucciones.")
	benefit = models.TextField(blank = True , null = True , verbose_name = "Define cuáles son los principales beneficios para tu colaborador al realziar ezta tarea.")
	next_task = models.TextField(blank = True , null = True , verbose_name = "Una vez concluida la tarea, cuál será la siguiente tarea que le delegarás?.")
	performance = models.ManyToManyField(sf_performance)
#	performance = models.ManyToManyField(ST_accion)
	comments = models.TextField(blank = True , null = True , verbose_name = "Comenta cuales fueron las evidencias que te confirmaron el compromiso de tu colaborador respecto a la tarea delegada.")

	def _formClass(self):
		from forms import SessionFiveForm
		return SessionFiveForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-III/sesion-5/base.html'

	@classmethod
	def getTotalQuestions(cls):
		return 7

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		if self.question_3_answered:
			total += 1
		if self.question_4_answered:
			total += 1
		if self.question_5_answered:
			total += 1
		if self.question_6_answered:
			total += 1
		if self.question_7_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	@classmethod
	def getPollIndex(cls):
		return 5

	@classmethod
	def getPollSectionIndex(cls):
		return 3

	@classmethod
	def getPollName(cls):
		return 'Sesión 5 - Delegación'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase III - Sesiones de Coaching'

	def save(self, *args, **kwargs):
		self.name = 'Sesión 5 - Delegación'
		self.section_name = 'Fase III - Sesiones de Coaching'
		self.section_index = 3
		self.index = 5
		super(SessionFive, self).save(*args, **kwargs)
	@classmethod
	def hasHeader(cls):
		return True
	@classmethod
	def getHeader(cls):
		header = "<p>De acuerdo al plan de acción definido con tu colaborador, establece una tarea que le ayude a lograr dicho plan y que le permita desarrollar una o varias habilidades requeridas para su mejora individual.</p>"
		header += "<p>Asegúrate de que la tarea cumpla con las 3 reglas de una buena asignación de tareas:</p>"
		header += "<ol>"
		header += "<li>que este ligada al plan de acción.</li>"
		header += "<li>que le permita un beneficio o desarrollo significativo.</li>"
		header += "<li>que este 100% en sus manos el poder ejecutarla.</li>"
		header += "</ol>"
		header += "<p>No olvides confirmar la claridad de la tarea y el compromiso.</p>"
		return header
	def _question_1_answered(self):
		return self.question_1_value and self.question_1_value.strip()
	question_1_answered = property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "1.- Describe la tarea que delegarás a tu colaborador."
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "Asegúrate que la tarea pueda ser delegada sin poner en riesgo un procedimiento o protocolo establecido."
		return header
	@classmethod
	def question_1_id(cls):
		return 'delegated_task'

	def _question_1_value(self):
		return self.delegated_task or ''
	question_1_value = property(_question_1_value)

	def _question_2_answered(self):
		return self.question_2_value and self.question_2_value.strip()
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "2.- Describe cómo es que esta tarea impacta positivamente al plan de acción."
	@classmethod
	def question_2_has_header(cls):
		return False
	@classmethod
	def question_2_header(cls):
		header = None
		return header
	@classmethod
	def question_2_id(cls):
		return 'task_impact'

	def _question_2_value(self):
		return self.task_impact or ''
	question_2_value = property(_question_2_value)

	def _question_3_answered(self):
		return self.question_3a_value and self.question_3a_value.strip() and self.question_3b_value and self.question_3b_value.strip() and self.question_3c_value and self.question_3c_value.strip()
	question_3_answered = property(_question_3_answered)
	@classmethod
	def question_3_title(cls):
		return "3.- Enlista los 3 elementos más relevantes que deberá contener tu explicación de instrucciones para tu colaborador."
	@classmethod
	def question_3_has_header(cls):
		return False
	@classmethod
	def question_3_header(cls):
		header = None
		return header
	@classmethod
	def question_3a_label(cls):
		return 'a) primer elemento de instrucciones.'
	@classmethod
	def question_3a_id(cls):
		return 'first_instruction'

	def _question_3a_value(self):
		return self.first_instruction or ''
	question_3a_value = property(_question_3a_value)
	@classmethod
	def question_3b_label(cls):
		return 'b) segundo elemento de instrucciones.'
	@classmethod
	def question_3b_id(cls):
		return 'second_instruction'

	def _question_3b_value(self):
		return self.second_instruction or ''
	question_3b_value = property(_question_3b_value)
	@classmethod
	def question_3c_label(cls):
		return 'c) tercer elemento de instrucciones.'
	
	@classmethod
	def question_3c_id(cls):
		return 'third_instruction'

	def _question_3c_value(self):
		return self.third_instruction or ''
	question_3c_value = property(_question_3c_value)

	def _question_4_answered(self):
		if self.benefit and self.benefit.split():
			return True
		return False
	question_4_answered = property(_question_4_answered)

	@classmethod
	def question_4_title(cls):
		return "4.- Define cuáles son los principales beneficios para tu colaborar al realizar esta tarea."
	@classmethod
	def question_4_has_header(cls):
		return False
	@classmethod
	def question_4_header(cls):
		header = None
		return header
	@classmethod
	def question_4_id(cls):
		return 'benefit'

	def _question_4_value(self):
		return self.benefit or ''
	question_4_value = property(_question_4_value)

	def _question_5_answered(self):
		if self.next_task and self.next_task.split():
			return True
		return False
	question_5_answered = property(_question_5_answered)
	@classmethod
	def question_5_title(cls):
		return "5.-Una vez concluida la tarea, cuál será la siguiente tarea que le delegarás?"
	@classmethod
	def question_5_has_header(cls):
		return False
	@classmethod
	def question_5_header(cls):
		header = None
		return header
	@classmethod
	def question_5_id(cls):
		return 'next_task'

	def _question_5_value(self):
		return self.next_task or ''
	question_5_value = property(_question_5_value)

	def _question_6_answered(self):
		return self.performancesCount > 0
	question_6_answered = property(_question_6_answered)

	def _performances(self):
		return self.performance.all()
	performances = property(_performances)

	def _performancesCount(self):
		return self.performances.count()
	performancesCount = property(_performancesCount)

	def addPerformance(self , performance = None , result = None):
		added = False
		if performance and performance.strip() and result and result.strip():
			instance = sf_performance.objects.create(performance = performance , result = result)
			if instance:
				self.performance.add(instance)
				self.save()
				added = True
				self.setUpdatedTimestamp(now = True)
		return added

	def removePerformance(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.performances.filter(id = id).first()
			if instance:
				self.performance.remove(instance)
				self.save()
				instance.delete()
				self.setUpdatedTimestamp(now = True)
				removed = True
		return removed

	def question_6_title(cls):
		return "6.- Define los indicadores clave de desempeño que impactarán positivamente esta tarea y los resultados esperados."
	@classmethod
	def question_6_has_header(cls):
		return False
	@classmethod
	def question_6_header(cls):
		header = None
		return header
	@classmethod
	def question_6_id(cls):
		return 'performance_id'
	@classmethod
	def question_6_value(cls):
		return ""
	def _question_7_answered(self):
		if self.comments and self.comments.split():
			return True
		return False
	question_7_answered = property(_question_7_answered)
	@classmethod
	def question_7_title(cls):
		return "7.- Comenta cuales fueron las evidencias que te confirmaron el compromiso de tu colaborador respecto a la tarea delegada."
	@classmethod
	def question_7_has_header(cls):
		return False
	@classmethod
	def question_7_header(cls):
		header = None
		return header
	@classmethod
	def question_7_id(cls):
		return 'comments'

	def _question_7_value(self):
		return self.comments or ''
	question_7_value = property(_question_7_value)
#################################[-------Sesion 6-----------]#################################################
class SessionSix(Base):
	positive_aspect_1 = models.TextField(blank = True , null = True , verbose_name = "Aspecto Positivo.")
	positive_aspect_2 = models.TextField(blank = True , null = True , verbose_name = "Aspecto Positivo.")
	positive_aspect_3 = models.TextField(blank = True , null = True , verbose_name = "Aspecto Positivo.")
	oportunity_1 = models.TextField(blank = True , null = True , verbose_name = "Área de Oportunidad.")
	oportunity_2 = models.TextField(blank = True , null = True , verbose_name = "Área de Oportunidad.")
	oportunity_3 = models.TextField(blank = True , null = True , verbose_name = "Área de Oportunidad.")
	alternative_1 = models.TextField(blank = True , null = True , verbose_name = "Alternativa.")
	alternative_2 = models.TextField(blank = True , null = True , verbose_name = "Alternativa.")
	alternative_3 = models.TextField(blank = True , null = True , verbose_name = "Alternativa.")
	next_step = models.TextField(blank = True , null = True , verbose_name = "Próximo Pasos.")
	renovation_dates = models.TextField(blank = True , null = True , verbose_name = "Fechas de Renovación.")
	comments = models.TextField(blank = True , null = True , verbose_name = "Comentarios Generales de la sesión.")

	def _formClass(self):
		from forms import SessionSixForm
		return SessionSixForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-III/sesion-6/base.html'

	@classmethod
	def getTotalQuestions(cls):
		return 5

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		if self.question_3_answered:
			total += 1
		if self.question_4_answered:
			total += 1
		if self.question_5_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	@classmethod
	def getPollIndex(cls):
		return 6

	@classmethod
	def getPollSectionIndex(cls):
		return 3

	@classmethod
	def getPollName(cls):
		return 'Sesión 6 - Retroalimentación'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase III - Sesiones de Coaching'

	def save(self, *args, **kwargs):
		self.name = 'Sesión 6 - Retroalimentación'
		self.section_name = 'Fase III - Sesiones de Coaching'
		self.section_index = 3
		self.index = 6
		super(SessionSix, self).save(*args, **kwargs)
	@classmethod
	def hasHeader(cls):
		return True
	@classmethod
	def getHeader(cls):
		header = "De acuerdo al plan de acción definido y a las evidencias de avances identificadas describe tys hallazgos como Coach."
		header += "</br>"
		header += "Llena el siguiente formulario de acuerdo con la fórmula para una retroalimentación constructiva."
		header += "</br>"
		header += "Recuerda que la retroalimentación debe generar motivación por los logros y la identificación de los aspectos de mejora que tu colaborador deberá tomar en cuenta para desarrollar nuevas o mayores habilidades."
		return header

	def _question_1_answered(self):
		return self.question_1a_value and self.question_1a_value.strip() and self.question_1b_value and self.question_1b_value.strip() and self.question_1c_value and self.question_1c_value.strip()
	question_1_answered = property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "1.- Describe los 3 aspectos positivos que has observado en tu colaborador."
	@classmethod
	def question_1_has_header(cls):
		return False
	@classmethod
	def question_1_header(cls):
		header = None
		return header
	@classmethod
	def question_1a_label(cls):
		return 'Aspecto Positivo'
	@classmethod
	def question_1a_id(cls):
		return 'positive_aspect_1'

	def _question_1a_value(self):
		return self.positive_aspect_1 or ''
	question_1a_value = property(_question_1a_value)
	@classmethod
	def question_1b_label(cls):
		return ''
	@classmethod
	def question_1b_id(cls):
		return 'positive_aspect_2'

	def _question_1b_value(self):
		return self.positive_aspect_2 or ''
	question_1b_value = property(_question_1b_value)
	@classmethod
	def question_1c_label(cls):
		return ''
	@classmethod
	def question_1c_id(cls):
		return 'positive_aspect_3'

	def _question_1c_value(self):
		return self.positive_aspect_3 or ''
	question_1c_value = property(_question_1c_value)

	def _question_2_answered(self):
		return self.question_2a_value and self.question_2a_value.strip() and self.question_2b_value and self.question_2b_value.strip() and self.question_2c_value and self.question_2c_value.strip()
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "2.- Establece las 3 áreas de opotunidad o mejora que hayas identificado."
	@classmethod
	def question_2_has_header(cls):
		return False
	@classmethod
	def question_2_header(cls):
		header = None
		return header
	@classmethod
	def question_2a_label(cls):
		return 'Áreas de Oportunidad'
	@classmethod
	def question_2a_id(cls):
		return 'oportunity_1'

	def _question_2a_value(self):
		return self.oportunity_1 or ''
	question_2a_value = property(_question_2a_value)
	@classmethod
	def question_2b_label(cls):
		return ''
	@classmethod
	def question_2b_id(cls):
		return 'oportunity_2'

	def _question_2b_value(self):
		return self.oportunity_2 or ''
	question_2b_value = property(_question_2b_value)
	@classmethod
	def question_2c_label(cls):
		return ''
	@classmethod
	def question_2c_id(cls):
		return 'oportunity_3'

	def _question_2c_value(self):
		return self.oportunity_3 or ''
	question_2c_value = property(_question_2c_value)

	def _question_3_answered(self):
		return self.question_3a_value and self.question_3a_value.strip() and self.question_3b_value and self.question_3b_value.strip() and self.question_3c_value and self.question_3c_value.strip()
	question_3_answered = property(_question_3_answered)
	@classmethod
	def question_3_title(cls):
		return "3.- Enlista las 3 alternativas o recomendaciones que tu le darás a tu colaborador para la mejora de su desempeño."
	@classmethod
	def question_3_has_header(cls):
		return False
	@classmethod
	def question_3_header(cls):
		header = None
		return header
	@classmethod
	def question_3a_label(cls):
		return 'Alternativas o Recomendaciones'
	@classmethod
	def question_3a_id(cls):
		return 'alternative_1'

	def _question_3a_value(self):
		return self.alternative_1 or ''
	question_3a_value = property(_question_3a_value)
	@classmethod
	def question_3b_label(cls):
		return ''
	@classmethod
	def question_3b_id(cls):
		return 'alternative_2'

	def _question_3b_value(self):
		return self.alternative_2 or ''
	question_3b_value = property(_question_3b_value)
	@classmethod
	def question_3c_label(cls):
		return ''
	@classmethod
	def question_3c_id(cls):
		return 'alternative_3'

	def _question_3c_value(self):
		return self.alternative_3 or ''
	question_3c_value = property(_question_3c_value)

	def _question_4_answered(self):
		return self.question_4a_value and self.question_4a_value.strip() and self.question_4b_value and self.question_4b_value.strip()
	question_4_answered = property(_question_4_answered)
	@classmethod
	def question_4_title(cls):
		return "4.- Junto con tu colaborador definan las próximos pasos para mejorar las áreas de oportunidad y las fechas de revisión."
	@classmethod
	def question_4_has_header(cls):
		return False
	@classmethod
	def question_4_header(cls):
		header = None
		return header
	@classmethod
	def question_4a_label(cls):
		return 'Próximos Pasos'
	@classmethod
	def question_4a_id(cls):
		return 'next_step'

	def _question_4a_value(self):
		return self.next_step or ''
	question_4a_value = property(_question_4a_value)
	@classmethod
	def question_4b_label(cls):
		return 'Fecha de Revisón'
	@classmethod
	def question_4b_id(cls):
		return 'renovation_dates'

	def _question_4b_value(self):
		return self.renovation_dates or ''
	question_4b_value = property(_question_4b_value)

	def _question_5_answered(self):
		return self.question_5_value and self.question_5_value.strip()
	question_5_answered = property(_question_5_answered)
	@classmethod
	def question_5_title(cls):
		return "Comentarios Generales de la sesión."
	@classmethod
	def question_5_has_header(cls):
		return False
	@classmethod
	def question_5_header(cls):
		header = None
		return header
	@classmethod
	def question_5_id(cls):
		return 'comments'

	def _question_5_value(self):
		return self.comments or ''
	question_5_value = property(_question_5_value)
#################################[-------Análisis de Avances-----------]#################################################
class AA_task(models.Model):
	description = models.TextField(blank = True , null = True , verbose_name = "Descripción")
	evidence = models.TextField(blank = True , null = True , verbose_name = "Evidencia")
	indicator = models.TextField(blank = True , null = True , verbose_name = "Indicador Establecido")
	result = models.TextField(blank = True , null = True , verbose_name = "Resultado Real")
	finished = models.NullBooleanField(verbose_name = "Tarea Concluida")
	comments = models.TextField(blank = True , null = True , verbose_name = "Comentarios Generales de la sesión.")

class AnalisisAvances(Base):
	task = models.ManyToManyField(AA_task)

	def _formClass(self):
		from forms import AnalisisAvancesForm
		return AnalisisAvancesForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-IV/analisis-avances/base.html'

	@classmethod
	def getTotalQuestions(cls):
		return 1

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	@classmethod
	def getPollIndex(cls):
		return 1

	@classmethod
	def getPollSectionIndex(cls):
		return 4

	@classmethod
	def getPollName(cls):
		return 'Análisis de Avances'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase IV - Análisis de Avances de Proceso'

	def save(self, *args, **kwargs):
		self.name = 'Análisis de Avances'
		self.section_name = 'Fase IV - Análisis de Avances de Proceso'
		self.section_index = 4
		self.index = 1
		super(AnalisisAvances, self).save(*args, **kwargs)

	def _question_1_answered(self):
		return self.tasksCount > 0
	question_1_answered = property(_question_1_answered)
		
	def _tasks(self):
		return self.task.all()
	tasks = property(_tasks)

	def _tasksCount(self):
		return self.tasks.count()
	tasksCount = property(_tasksCount)
	
	def addTask(self , description = None , evidence = None , indicator = None , result = None , finished = None , comments = None):
		added = True
		if description and description.strip() and evidence and evidence.strip() and indicator and indicator.strip() and result and result.strip() and comments and comments.strip():
			instance = AA_task.objects.create(description = description , evidence = evidence , indicator = indicator , result = result , finished = finished , comments = comments)
			if instance:
				self.task.add(instance)
				self.save()
				added = True
				self.setUpdatedTimestamp(now = True)
		return added
		
	def removeTask(self , id = None):
		removed = False
		if id and id.strip():
			instance = self.tasks.filter(id = id).first()
			if instance:
				self.task.remove(instance)
				removed = True
				instance.delete()
				self.setUpdatedTimestamp(now = True)
		return removed

	@classmethod
	def question_1_title(cls):
		return "1.- Revisión del plan de acción."
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "De acuerdo al Plan de Acción establecido con tu colaborador verifica los avances de las tareas asignadas."
		return header
	@classmethod
	def question_1_id(cls):
		return 'task_id'
	@classmethod
	def question_1_value(cls):
		return ""
#################################[-------Reporte Final de Coaching-----------]#################################################
class ReporteFinalCoaching(Base):
	initial_situation = models.TextField(blank = True , null = True , verbose_name = "Situación Inicial" , help_text = "Describe la situación inicial en el cual encontraste al colaborador al inicio del proceso:")
	goal = models.TextField(blank = True , null = True , verbose_name = "Meta definida para el proceso de Coaching" , help_text = "Describe la meta acordada con tu colaborador para trabajar con tu intervención como Coach")
	final_status = models.TextField(blank = True , null = True , verbose_name = "Situación Final del desempeño" , help_text = "Describe los principales logros mostrados con tu intervención como Coach")
	main_change = models.TextField(blank = True , null = True , verbose_name = "Principales cambios para la mejora identificado" , help_text = "Describe los principales logros mostrados con tu intervención como Coach")
	main_difficulty = models.TextField(blank = True , null = True , verbose_name = "Principales dificultades enfrentadas durante el proceso")
	conclution = models.TextField(blank = True , null = True , verbose_name = "Conclusiones finales como Coach")

	def _formClass(self):
		from forms import ReporteFinalCoachingForm
		return ReporteFinalCoachingForm
	formClass = property(_formClass)

	@classmethod
	def template(cls):
		return 'system/polls/templates/Fase-V/reporte-final/base.html'

	@classmethod
	def getTotalQuestions(cls):
		return 6

	def _totalAnswered(self):
		total = 0
		if self.question_1_answered:
			total += 1
		if self.question_2_answered:
			total += 1
		if self.question_3_answered:
			total += 1
		if self.question_4_answered:
			total += 1
		if self.question_5_answered:
			total += 1
		if self.question_6_answered:
			total += 1
		return total
	totalAnswered = property(_totalAnswered)

	@classmethod
	def getPollIndex(cls):
		return 1

	@classmethod
	def getPollSectionIndex(cls):
		return 5

	@classmethod
	def getPollName(cls):
		return 'Reporte Final de Coaching'

	@classmethod
	def getPollSectionName(cls):
		return 'Fase V - Cierre de Proceso'

	def save(self, *args, **kwargs):
		self.name = 'Reporte Final de Coaching'
		self.section_name = 'Fase V - Cierre de Proceso'
		self.section_index = 5
		self.index = 1
		super(ReporteFinalCoaching, self).save(*args, **kwargs)

	def _question_1_answered(self):
		return self.question_1_value and self.question_1_value.strip()
	question_1_answered = property(_question_1_answered)
	@classmethod
	def question_1_title(cls):
		return "1.- Situación Inicial"
	@classmethod
	def question_1_has_header(cls):
		return True
	@classmethod
	def question_1_header(cls):
		header = "Describe la situación inicial en el cual encontraste al colaborador al inicio del proceso:"
		return header
	@classmethod
	def question_1_id(cls):
		return 'initial_situation'

	def _question_1_value(self):
		return self.initial_situation or ''
	question_1_value = property(_question_1_value)

	def _question_2_answered(self):
		return self.question_2_value and self.question_2_value.strip()
	question_2_answered = property(_question_2_answered)
	@classmethod
	def question_2_title(cls):
		return "2.- Meta definida para el proceso de Coaching"
	@classmethod
	def question_2_has_header(cls):
		return True
	@classmethod
	def question_2_header(cls):
		header = "Describe la meta acordada con tu colaborador para trabajar con tu intervención como Coach"
		return header
	@classmethod
	def question_2_id(cls):
		return 'goal'

	def _question_2_value(self):
		return self.goal or ''
	question_2_value = property(_question_2_value)

	def _question_3_answered(self):
		return self.question_3_value and self.question_3_value.strip()
	question_3_answered = property(_question_3_answered)
	@classmethod
	def question_3_title(cls):
		return "3.- Situación Final del desempeño"
	@classmethod
	def question_3_has_header(cls):
		return True
	@classmethod
	def question_3_header(cls):
		header = "Describe los principales logros mostrados con tu intervención como Coach"
		return header
	@classmethod
	def question_3_id(cls):
		return 'final_status'

	def _question_3_value(self):
		return self.final_status or ''
	question_3_value = property(_question_3_value)

	def _question_4_answered(self):
		return self.question_4_value and self.question_4_value.strip()
	question_4_answered = property(_question_4_answered)
	@classmethod
	def question_4_title(cls):
		return "4.- Principales cambios para la mejora identificados"
	@classmethod
	def question_4_has_header(cls):
		return True
	@classmethod
	def question_4_header(cls):
		header = "Describe las principales actitudes mostradas con tu intervención como Coach"
		return header
	@classmethod
	def question_4_id(cls):
		return 'main_change'

	def _question_4_value(self):
		return self.main_change or ''
	question_4_value = property(_question_4_value)

	def _question_5_answered(self):
		return self.question_5_value and self.question_5_value.strip()
	question_5_answered = property(_question_5_answered)
	@classmethod
	def question_5_title(cls):
		return "5.- Principales dificultades enfrentadas durante el proceso"
	@classmethod
	def question_5_has_header(cls):
		return False
	@classmethod
	def question_5_header(cls):
		header = None
		return header
	@classmethod
	def question_5_id(cls):
		return 'main_difficulty'

	def _question_5_value(self):
		return self.main_difficulty or ''
	question_5_value = property(_question_5_value)

	def _question_6_answered(self):
		return self.question_6_value and self.question_6_value.strip()
	question_6_answered = property(_question_6_answered)
	@classmethod
	def question_6_title(cls):
		return "6.- Conclusiones finales como Coach"
	@classmethod
	def question_6_has_header(cls):
		return False
	@classmethod
	def question_6_header(cls):
		header = None
		return header
	@classmethod
	def question_6_id(cls):
		return 'conclution'

	def _question_6_value(self):
		return self.conclution or ''
	question_6_value = property(_question_6_value)