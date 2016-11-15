from django.db import models
from django.conf import settings
from ipware.ip import get_ip
from django.contrib.auth.models import User

class Browser(models.Model):
	family = models.CharField(max_length = 250 , blank = False , null = False)
	version_string = models.CharField(max_length = 250 , blank = False , null = False)
	version = models.IntegerField(blank = False , null = False , default = -1)
	subversion = models.IntegerField(blank = False , null = False , default = -1)
	
	def __unicode__(self):
		return "%s - %s" % (self.family , self.version_string)
		
	class Meta:
		ordering = ['family' , 'version' , 'subversion']
		
	@classmethod
	def create_obj(cls , obj):
		family = obj.family
		version_string = obj.version_string
#		version , subversion = obj.version
#		obj , created = cls.objects.get_or_create(family = family , version_string = version_string , version = version , subversion = subversion)
		obj , created = cls.objects.get_or_create(family = family , version_string = version_string)
		return obj

class OS(models.Model):
	family = models.CharField(max_length = 250 , blank = False , null = False)
	version_string = models.CharField(max_length = 250 , blank = False , null = False)
	version = models.IntegerField(blank = False , null = False , default = -1)
	subversion = models.IntegerField(blank = False , null = False , default = -1)
	
	def __unicode__(self):
		return "%s - %s" % (self.family , self.version_string)
		
	class Meta:
		ordering = ['family' , 'version' , 'subversion']

	@classmethod
	def create_obj(cls , obj):
		family = obj.family
		version_string = obj.version_string
#		version , subversion = obj.version
#		obj , created = cls.objects.get_or_create(family = family , version_string = version_string , version = version , subversion = subversion)
		obj , created = cls.objects.get_or_create(family = family , version_string = version_string)
		return obj
		
class Device(models.Model):
	family = models.CharField(max_length = 250 , blank = False , null = False)
	is_mobile = models.BooleanField(blank = False , null = False , default = False)
	is_tablet = models.BooleanField(blank = False , null = False , default = False)
	is_pc = models.BooleanField(blank = False , null = False , default = False)
	is_touch_capable = models.BooleanField(blank = False , null = False , default = False)
	is_bot = models.BooleanField(blank = False , null = False , default = False)
	
	def __unicode__(self):
		return "%s - is_mobile:%s - is_tablet:%s - is_pc:%s - is_touch_capable:%s - is_bot:%s" % (self.family , self.is_mobile , self.is_tablet , self.is_pc , self.is_touch_capable , self.is_bot)
		
	class Meta:
		ordering = ['family' , 'is_mobile' , 'is_tablet' , 'is_pc' , 'is_touch_capable' , 'is_bot']

	@classmethod
	def create_obj(cls , obj):
		family = obj.device.family
		is_mobile = obj.is_mobile
		is_tablet = obj.is_tablet
		is_pc = obj.is_pc
		is_touch_capable = obj.is_touch_capable
		is_bot = obj.is_bot
		obj , created = cls.objects.get_or_create(family = family , is_mobile = is_mobile , is_tablet = is_tablet , is_pc = is_pc , is_touch_capable = is_touch_capable , is_bot = is_bot)
		return obj

class Server(models.Model):
	name = models.CharField(max_length = 250 , blank = False , null = False)
	port = models.CharField(max_length = 250 , blank = False , null = False)

class LocalResource(models.Model):
	absolute_uri = models.URLField(blank = False , null = False)
	path = models.CharField(max_length = 250 , blank = False , null = False)
	path_info = models.CharField(max_length = 250 , blank = False , null = False)
	full_path = models.CharField(max_length = 250 , blank = False , null = False)
	content_type = models.CharField(max_length = 250 , blank = True , null = True)
	domain = models.ForeignKey('Domain' , blank = False , null = False)
	server = models.ForeignKey('Server' , blank = False , null = False)
	ajax = models.BooleanField(blank = False , null = False , default = False)
	query_string = models.CharField(max_length = 250 , blank = True , null = True)
	method = models.CharField(max_length = 250 , blank = False , null = False)
	
class Domain(models.Model):
	host = models.CharField(max_length = 250 , blank = False , null = False)
	http_host = models.CharField(max_length = 250 , blank = False , null = False)
	secure = models.BooleanField(blank = False , null = False , default = False)
	
class Reference(models.Model):
	absolute_uri = models.URLField(blank = False , null = False)
	local_resource = models.ForeignKey('LocalResource' , blank = True , null = True)
	path = models.CharField(max_length = 250 , blank = True , null = True)
	query_string = models.CharField(max_length = 250 , blank = True , null = True)
	
	
	def save(self, *args, **kwargs):
		if self.absolute_uri and self.local_resource is None:
			if self.path is None and self.query_string is None:
				from urlparse import urlparse
				url = self.absolute_uri
				if url and url.strip():
					path = None
					query_string = None
					try:
						o = urlparse(url)
						path = o.path or None
						query_string = o.query or None
					except:
						pass
					self.path = path
					self.query_string = query_string
#			print "%s" % self.absolute_uri
			if self.path:
#				print "Begin to Search"
				resources = LocalResource.objects.filter(path = self.path)
#				print "resources.count() : %s" % resources.count()
				if resources.count() > 0:
					if self.query_string:
#						print "self.query_string : %s" % self.query_string
						resource = resources.filter(query_string = self.query_string).first()
#						print "resource : %s" % resource
						if resource:
							self.local_resource = resource
						else:
							resource = resources.first()
#							print "resource SECOND : %s" % resource
							if resource:
								self.local_resource = resource
					else:
						resource = resources.first()
#						print "resource Third : %s" % resource
						if resource:
							self.local_resource = resource
#			try:
#				self.local_resource = LocalResource.objects.get(absolute_uri = self.absolute_uri)
#			except:
#				pass
		super(Reference, self).save(*args, **kwargs)

	
class Guest(models.Model):
	remote_addr = models.GenericIPAddressField(blank = False , null = False , default = '')
	remote_host = models.CharField(max_length = 250 , blank = True , null = True , default = '')
	remote_user = models.CharField(max_length = 250 , blank = True , null = True , default = '')
	fetched = models.BooleanField(blank = False , null = False , default = False)
	fetched_hostname = models.CharField(max_length = 250 , blank = True , null = True , default = None)
	fetched_city = models.CharField(max_length = 250 , blank = True , null = True , default = None)
	fetched_region = models.CharField(max_length = 250 , blank = True , null = True , default = None)
	fetched_contry = models.CharField(max_length = 250 , blank = True , null = True , default = None)
	fetched_loc = models.CharField(max_length = 250 , blank = True , null = True , default = None)
	fetched_org = models.CharField(max_length = 250 , blank = True , null = True , default = None)
	fetched_postal = models.CharField(max_length = 250 , blank = True , null = True , default = None)
	
	def _detail(self):
		detail = ""
		
		return detail
	detail = property(_detail)
	
	def save(self, *args, **kwargs):
		if self.remote_addr and self.remote_addr.strip():
			import requests
			import traceback
			import sys
			ip = self.remote_addr.strip()
			try:
				ipinfo = requests.get('http://ipinfo.io/%s/json' % ip)
				json = ipinfo.json()
				self.fetched_hostname = json.get('hostname') or None
				self.fetched_city = json.get('city') or None
				self.fetched_region = json.get('region') or None
				self.fetched_contry = json.get('country') or None
				self.fetched_loc = json.get('loc') or None
				self.fetched_org = json.get('org') or None
				self.fetched_postal = json.get('postal') or None
				self.fetched = True
			except Exception,e:
				print "%s" % e
				print(traceback.format_exc())
				self.fetched = False
				self.fetched_hostname = None
				self.fetched_city = None
				self.fetched_region = None
				self.fetched_contry = None
				self.fetched_loc = None
				self.fetched_org = None
				self.fetched_postal = None
		super(Guest, self).save(*args, **kwargs)

class Hit(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True , blank = True , null = False)
##	local_timestamp = models.DateTimeField(blank = True , null = True)
	guest = models.ForeignKey('Guest' , blank = False , null = False)
	reference = models.ForeignKey('Reference' , blank = True , null = True)
	local_resource = models.ForeignKey('LocalResource' , blank = False , null = False)
	device = models.ForeignKey('Device' , blank = False , null = False)
	os = models.ForeignKey('OS' , blank = False , null = False)
	browser = models.ForeignKey('Browser' , blank = False , null = False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL , blank = True , null = True)
	
	def _page(self):
		page = ""
		if self.local_resource:
			page = self.local_resource.path or ""
		return page
	page = property(_page)
	
	def _referencePage(self):
		page = "No Reference"
		if self.reference:
			page = self.reference.path or "No Reference"
		return page
	referencePage = property(_referencePage)
	
	def _date(self):
		return self.timestamp
	date = property(_date)
	
	def _dateLabel(self):
		from datetime import datetime
		from pytz import timezone
		date = self.date
		if date:
			date_str = date.strftime("%Y-%m-%d %H:%M:%S")
			datetime_obj_naive = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
			datetime_obj_utc = timezone('UTC').localize(datetime_obj_naive)
			localTimeStamp = datetime_obj_utc.astimezone(timezone('US/Central'))
			op_orderDate = localTimeStamp.strftime(("%Y-%m-%d %H:%M:%S"))
			return op_orderDate
		return "NO DATE"
	dateLabel = property(_dateLabel)
	
##	def save(self, *args, **kwargs):
##		if self.timestamp and self.local_timestamp is None:
##			from datetime import datetime
##			from pytz import timezone
##			op_orderDate = ""
##			if self.timestamp:
##				timestamp = self.timestamp
##				date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
##				datetime_obj_naive = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
##				datetime_obj_utc = timezone('UTC').localize(datetime_obj_naive)
##				localTimeStamp = datetime_obj_utc.astimezone(timezone('US/Central'))
##				self.local_timestamp = localTimeStamp
###	#			localTimeStamp = self.checkouted_timestamp.astimezone(timezone('US/Central'))
###				op_orderDate = localTimeStamp.strftime("%Y-%m-%d")
##		super(Hit, self).save(*args, **kwargs)

	@classmethod
	def page_visited(cls , request = None):
		hit = None
		ip = get_ip(request)
		if request and settings.ANALYTICS_RECORD:
			if request.user.is_authenticated():
				user = request.user
			else:
				user = None
			guest = None
			domain = None
			server = None
			local_resource = None
			reference = None
			browser = None
			os = None
			device = None
			if request.META:
				try:
					ip = get_ip(request)
				except:
					ip = None
				if ip is None:
					x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR') or None
					if x_forwarded_for:
						ip = x_forwarded_for.split(',')[0]
					else:
						ip = request.META.get('REMOTE_ADDR')
				if ip:
					remote_addr = ip
				else:
					remote_addr = request.META.get('REMOTE_ADDR') or None
				remote_host = request.META.get('REMOTE_HOST') or None
				remote_user = request.META.get('REMOTE_USER') or None
				http_host = request.META.get('HTTP_HOST') or None
				host = request.get_host()
				server_name = request.META.get('SERVER_NAME') or '127.0.0.1'
				server_port = request.META.get('SERVER_PORT') or '80'
				secure = request.is_secure()
				absolute_uri = request.build_absolute_uri()
				path = request.path
				path_info = request.path_info
				full_path = request.get_full_path()
				content_type = request.META.get('CONTENT_TYPE') or None
				ajax = request.is_ajax()
				query_string = request.META.get('QUERY_STRING') or None
				try:
					if query_string is None:
						qs = "GET:%s" % request.GET.dict()
						qs += "POST:%s" % request.POST.dict()
						query_string = qs
					else:
						qs = "GET:%s" % request.GET.dict()
						qs += "POST:%s" % request.POST.dict()
						query_string += qs
				except Exception , e:
					query_string = str(e)
				method = request.method
				http_referer = request.META.get('HTTP_REFERER') or None
				from user_agents import parse
				if request.META.get('HTTP_USER_AGENT') or None:
					user_agent = parse(request.META.get('HTTP_USER_AGENT'))
					browser = Browser.create_obj(user_agent.browser)
					os = OS.create_obj(user_agent.os)
					device = Device.create_obj(user_agent)
				if remote_addr:
					guest , created = Guest.objects.get_or_create(remote_addr = remote_addr , remote_host = remote_host , remote_user = remote_user)
					if guest:
						guest.save()
				if http_host:
					domain , created = Domain.objects.get_or_create(host = host , http_host = http_host , secure = secure)
				if server_name and server_port:
					server , created = Server.objects.get_or_create(name = server_name , port = server_port)
				if server and domain:
					local_resource , created = LocalResource.objects.get_or_create(absolute_uri = absolute_uri , path = path , path_info = path_info , full_path = full_path , content_type = content_type , ajax = ajax , query_string = query_string , method = method , domain = domain , server = server)
				if http_referer:
					reference , created = Reference.objects.get_or_create(absolute_uri = http_referer)
				if guest and local_resource and device and os and browser:
					hit = cls.objects.create(guest = guest , reference = reference , local_resource = local_resource , device = device , os = os , browser = browser , user = user)
		return hit

	@classmethod
	def executiveReport(cls , data = []):
		if data is None or len(data) == 0:
			return {
				'paths' : {
							'count' : 0 ,
							'lists' : []
						} ,
				'all' : 0 ,
				'year' : 0 ,
				'month' : 0 ,
				'week' : 0 ,
				'day' : 0 ,
			}
		import datetime
		from datetime import date, timedelta
		from django.db.models import Count
		now = datetime.datetime.now()
		today = now.today()
		weekday = now.weekday()
		year = now.year
		day = now.day
		month = now.month
		beginOfWeek = now.today() - timedelta(days = 7)
		endDate = now.strftime("%Y-%m-%d")
		beginDate = beginOfWeek.strftime("%Y-%m-%d")
		#############################COUNT OF THE DAY
		todayData = data.filter(timestamp__year = year)
		todayData = todayData.filter(timestamp__month = month)
		todayData = todayData.filter(timestamp__day = day)
		todayCount = todayData.count()
		#############################COUNT OF THE DAY
		#############################COUNT OF THE WEEK
		weekData = data.filter(timestamp__range=[beginDate , endDate])
		weekCount = weekData.count()
		#############################COUNT OF THE WEEK
		#############################COUNT OF THE MONTH
		monthData = data.filter(timestamp__year = year)
		monthData = monthData.filter(timestamp__month = month)
		monthCount = monthData.count()
		#############################COUNT OF THE MONTH
		#############################COUNT OF THE YEAR
		yearData = data.filter(timestamp__year = year)
		yearCount = yearData.count()
		#############################COUNT OF THE YEAR
		allCount = data.count()
		paths_data = data.values('local_resource__path' , 'local_resource__id').annotate(hits=Count('local_resource__path')).order_by('-hits' , 'local_resource__path')
		paths = {
			'count' : paths_data.count() ,
			'lists' : [ { 'id' : p.get('local_resource__id') , 'path' : p.get('local_resource__path') , 'hits' : p.get('hits') , } for p in paths_data ]
		}
		report = {
			'paths' : paths ,
			'all' : allCount ,
			'year' : yearCount ,
			'month' : monthCount ,
			'week' : weekCount ,
			'day' : todayCount ,
		}
		return report
		
	@classmethod
	def printableList(cls , data = []):
		return data