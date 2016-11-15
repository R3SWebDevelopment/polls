from django.db import models
from django.conf import settings
import traceback
import sys
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.contrib.auth.models import User

class Email(models.Model):
	address = models.CharField(max_length=250 , unique = True)
	
	@classmethod
	def add(cls , address = None):
		instance = None
		if address and address.strip():
			instance , created = cls.objects.get_or_create(address = address)
		return instance

class EmailTracker(models.Model):
	parent = models.ForeignKey(User, blank = True , null = True , default = None)
	parent = models.ForeignKey('EmailTracker', blank = True , null = True , default = None)
	sender = models.ForeignKey(Email, blank = True , null = True , default = None)
	htmlContent = models.TextField(default = None , null = True , blank = True)
	textContent = models.TextField(default = None , null = True , blank = True)
	subject = models.CharField(max_length=250 , default = None , null = True , blank = True)
	created = models.DateTimeField(auto_now_add=True , null = True , blank = True)
	sent = models.DateTimeField(default = None , null = True , blank = True)
	success = models.NullBooleanField(default = False)
	errorMessage = models.TextField(default = None , null = True , blank = True)
	testing = models.NullBooleanField(default = False)
	backTrack = models.TextField(default = None , null = True , blank = True)
	recipient = models.ManyToManyField(Email , related_name = "mail_recepient")
	cc = models.ManyToManyField(Email , related_name = "mail_cc")
	bcc = models.ManyToManyField(Email , related_name = "mail_bcc")
	kind = models.CharField(max_length=250 , default = None , null = True , blank = True)
	
	class Meta:
		ordering = ['sent']
		
	def _date(self):
		from datetime import datetime
		from pytz import timezone
		date = self.sent or self.created or None
		if date:
			timestamp = date
			date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
			datetime_obj_naive = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
			datetime_obj_utc = timezone('UTC').localize(datetime_obj_naive)
			localTimeStamp = datetime_obj_utc.astimezone(timezone('US/Central'))
#			localTimeStamp = self.checkouted_timestamp.astimezone(timezone('US/Central'))
			date = localTimeStamp.strftime("%Y-%m-%d")
		return date
	date = property(_date)

	def _subjectText(self):
		name = None
		if self.subject:
			name = self.subject
		return name
	subjectText = property(_subjectText)
	
	def _recepientsText(self):
		name = None
		recipients = self.recipients or []
		name = ", ".join(recipients)
		return name
	recepientsText = property(_recepientsText)
	
	def _ccText(self):
		name = None
		cc = self.CC or []
		name = ", ".join(cc)
		return name
	ccText = property(_ccText)
	
	def _bccText(self):
		name = None
		bcc = self.BCC or []
		name = ", ".join(bcc)
		return name
	bccText = property(_bccText)
	
	def _wasSent(self):
		return self.success or False
	wasSent = property(_wasSent)

	def addRecepient(self , address = None):
		address = Email.add(address = address)
		if address:
			if not self.recipient.filter(address = address).exists():
				self.recipient.add(address)

	def addCC(self , address = None):
		address = Email.add(address = address)
		if address:
			if not self.cc.filter(address = address).exists():
				self.cc.add(address)

	def addBCC(self , address = None):
		address = Email.add(address = address)
		if address:
			if not self.bcc.filter(address = address).exists():
				self.bcc.add(address)

	def addSender(self , address = None):
		address = Email.add(address = address)
		if address:
			if self.sender is None:
				self.sender = address
				self.save()

	def _senderAddress(self):
		address = None
		if self.sender:
			address = self.sender.address or None
		return address
	senderAddress = property(_senderAddress)

	def _recipients(self):
		addresses = self.recipient.all().distinct()
		addresses = [ address.address for address in addresses]
		return addresses
	recipients = property(_recipients)

	def _CC(self):
		addresses = self.cc.all().distinct()
		addresses = [ address.address for address in addresses]
		return addresses
	CC = property(_CC)

	def _BCC(self):
		addresses = self.bcc.all().distinct()
		addresses = [ address.address for address in addresses]
		return addresses
	BCC = property(_BCC)
	
	def _mailSubject(self):
		return self.subject or ''
	mailSubject = property(_mailSubject)

	def _mailHTML(self):
		return self.htmlContent or ''
	mailHTML = property(_mailHTML)

	def _mailText(self):
		return self.textContent or ''
	mailText = property(_mailText)
	
	def save(self, *args, **kwargs):
		if self.pk is None:
			self.testing = settings.DEBUG or False
			backTrack = ''
			try:
				raise Exception('Fetching backTrack')
			except:
				try:
					backTrack = traceback.extract_stack()
					backTrack = ''.join(traceback.format_list(backTrack))
				except:
					backTrack = traceback.format_exc()
			self.backTrack = backTrack
		super(EmailTracker, self).save(*args, **kwargs)
		
	@classmethod
	def add(cls , recipient = None , html = None , content = None , subject = None , parent = None):
		if recipient and len(recipient) > 0:
			email = cls.objects.create(htmlContent = html , textContent = content , subject = subject , parent = parent)
			if email:
				for address in recipient:
					email.addRecepient(address = address)
				email.addSender(address = settings.RESET_SENDER)
				for address in settings.CC_PURCHASE_NOTIFICATIN_RECEPIENT:
					email.addBCC(address = address)
			return email
		return None	
		
	@classmethod
	def send(cls , recipient = None , html = None , content = None , subject = None , parent = None):
		sent = False
		email = cls.add(recipient = recipient , html = html , content = content , subject = subject , parent = parent)
		if email:
			sent = email.doSend
		return sent
		
	def _doSend(self):
		try:
			subject = self.mailSubject
			text_content = self.mailText
			if self.testing:
				recepients = [settings.TEST_RECIPIENTS]
				print "self.recipients: %s" % self.recipients
				bcc = []
				print "self.BCC: %s" % self.BCC
				cc = []
				print "self.CC: %s" % self.CC
			else:
				recepients = self.recipients
				bcc = self.BCC
				cc = self.CC
			sender = self.senderAddress
			html_content = self.mailHTML
			if sender and sender.strip():
				if html_content and html_content.strip():
					if len(recepients) > 0:
						msg = EmailMultiAlternatives(subject, text_content, sender , recepients , bcc=bcc , cc=cc)
						msg.attach_alternative(html_content, "text/html")
						msg.send()
						self.doSuccess
					else:
						self.addException(exception = Exception('No Recepient Address'))
				else:
					self.addException(exception = Exception('No Content'))
			else:
				self.addException(exception = Exception('No Sender Address'))
		except Exception , e:
			self.addException(exception = e)
		return self.success or False
	doSend = property(_doSend)
	
	def addException(self , exception = None):
		if exception:
			self.errorMessage = str(exception)
			self.success = False
			self.save()
	def _doSuccess(self):
		self.sent = datetime.now()
		self.success = True
		self.save()		
	doSuccess = property(_doSuccess)
