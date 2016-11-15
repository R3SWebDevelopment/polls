from django.db import models
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from slugify import slugify
import random, string
IMAGE_UPLOAD_TO_PATH = 'imagery'
NO_IMAGE_AVAILABLE = "%s%s/no-image.jpg" % (settings.MEDIA_URL , IMAGE_UPLOAD_TO_PATH)

class Album(models.Model):
	title = models.CharField(max_length = 250 , null = False , blank = True)
	subtitle = models.CharField(max_length = 250 , null = False , blank = True)
	description = models.TextField(null = False , blank = True)
	active = models.NullBooleanField(default = True)
	published = models.NullBooleanField(default = True)
	created_timestamp = models.DateTimeField(auto_now_add = True)
	updated_timestamp = models.DateTimeField(auto_now = True)
	order = models.PositiveSmallIntegerField(default = 0)
	can_remove = models.NullBooleanField(default = True)
	gallery = models.NullBooleanField(default = True)
	cover = models.NullBooleanField(default = False)

	def _imageCount(self):
		return self.images.count()
	imageCount = property(_imageCount)
	
	def removeImage(self , image = None):
		pass
		
	def addImage(self , image = None):
		pass
		
	def hasImage(self , image = None):
		pass
		
	def setImageOrder(self , image = None , index = 0):
		pass
		
	def _images(self):
		return self.images.exclude(active = False)
	getImages = property(_images)
	
	def _publishedImages(self):
		return self.images.exclude(active = False).exclude(published = False)
	getPublishedImages = property(_publishedImages)
	
	def _noImageListHtml(self):
		pass
	noImageListHtml = property(_noImageListHtml)
	
	def _imageListHtml(self):
		pass
	_imageListHtml = property(_imageListHtml)
	
	def _imageGrid(self):
		pass
	imageGrid = property(_imageGrid)
	
	def _imageGridDetailHtml(self):
		pass
	imageGridDetailHtml = property(_imageGridDetailHtml)
	
	def addImage(self , image = None):
		if image:
			instance , created = AlbumImage.objects.get_or_create(image = image , album = self)
			if created:
				pass
			elif instance.active is False:
				instance.reactive()
			return instance
		return None
		
	def _get_cover(self):
		images = self.getPublishedImages
		cover = images.filter(cover = True).first()
		if cover is None:
			cover = images.first()
		return cover
	get_cover = property(_get_cover)
	
	def _cover_url(self):
		cover_url = ''
		cover = self.get_cover
		if cover:
			cover_url = cover.url
		return cover_url
	cover_url = property(_cover_url)

class Image(models.Model):
	image = models.ImageField(upload_to = IMAGE_UPLOAD_TO_PATH , max_length = 250)
	slug = models.SlugField(max_length = 250)
	created_timestamp = models.DateTimeField(auto_now_add = True)

	def _url(self):
		if self.image:
			return self.image.url
		return ""
	url = property(_url)

	def save(self, *args, **kwargs):
		if self.image:
			name = self.image.name or None
			if name:
				slug = slugify( name , separator = "_")
				while self.__class__.objects.all().filter(slug = slug).count() > 0:
					length = 5
					prefix = "_%s" % ''.join(random.choice(string.lowercase) for i in range(length))
					prefix = slugify( prefix.lower() , separator = "_")
					slug = "%s%s" % (slug , prefix)
				self.slug = slug
		super(Image, self).save(*args, **kwargs)

	def _url(self):
		import os
		path = "%s/%s" % (settings.MEDIA_ROOT , self.image.name)
		exists = os.path.isfile(path)
		if os.path.isfile(path):
			return self.image.url
		return NO_IMAGE_AVAILABLE
	url = property(_url)
	
	def _create_timestamp_label(self):
		label = ''
		if self.created_timestamp:
			label = self.created_timestamp.strftime('%b, %d %Y - %H:%M:%S - %Z (%z)')
		return label
	create_timestamp_label = property(_create_timestamp_label)
	
	def _roundHtml(self):
		try:
			html = render_to_string('imagery/image/holder.html', { 'image': self , 'image_shape' : 'img-rounded' })
		except:
			html = ''
		return html
	roundHtml = property(_roundHtml)

	def _circleHtml(self):
		try:
			html = render_to_string('imagery/image/holder.html', { 'image': self , 'image_shape' : 'img-circle' })
		except:
			html = ''
		return html
	circleHtml = property(_circleHtml)

	def _thumbnailHtml(self):
		try:
			html = render_to_string('imagery/image/holder.html', { 'image': self , 'image_shape' : 'img-thumbnail' })
		except:
			html = ''
		return html
	thumbnailHtml = property(_thumbnailHtml)

class AlbumImage(models.Model):
	album = models.ForeignKey('Album' , related_name="images")
	image = models.ForeignKey('Image' , related_name="albums")
	title = models.CharField(max_length = 250 , null = False , blank = True , default = '')
	subtitle = models.CharField(max_length = 250 , null = False , blank = True , default = '')
	description = models.TextField(null = False , blank = True , default = '')
	active = models.NullBooleanField(default = True)
	published = models.NullBooleanField(default = True)
	cover = models.NullBooleanField(default = False)
	created_timestamp = models.DateTimeField(auto_now_add = True , null = True)
	updated_timestamp = models.DateTimeField(auto_now = True , null = True)
	published_timestamp = models.DateTimeField(default = None , null = True)
	order = models.PositiveSmallIntegerField(default = 0)

	class Meta:
		ordering = ["order"]

	def _url(self):
		if self.image:
			return self.image.url
		return ""
	url = property(_url)

	def _adminViewThumbnailHtml(self):
		pass
	adminViewThumbnailHtml = property(_adminViewThumbnailHtml)
	
	def _adminEditThumbnailHtml(self):
		pass
	adminEditThumbnailHtml = property(_adminEditThumbnailHtml)

	def _adminGridRoundHtml(self):
		pass
	adminGridRoundHtml = property(_adminGridRoundHtml)
	
	def _adminGridCircleHtml(self):
		pass
	adminGridCircleHtml = property(_adminGridCircleHtml)
	
	def _adminGridThumbnaulHtml(self):
		pass
	adminGridThumbnaulHtml = property(_adminGridThumbnaulHtml)

	def _create_timestamp_label(self):
		label = ''
		if self.created_timestamp:
			label = self.created_timestamp.strftime('%b, %d %Y - %H:%M:%S - %Z (%z)')
		return label
	create_timestamp_label = property(_create_timestamp_label)
	
	def _updated_timestamp_label(self):
		label = ''
		if self.updated_timestamp:
			label = self.updated_timestamp.strftime('%b, %d %Y - %H:%M:%S - %Z (%z)')
		return label
	updated_timestamp_label = property(_updated_timestamp_label)
	
	def _published_timestamp_label(self):
		label = ''
		if self.published_timestamp:
			label = self.published_timestamp.strftime('%b, %d %Y - %H:%M:%S - %Z (%z)')
		return label
	published_timestamp_label = property(_published_timestamp_label)

	def setOrder(self , index = None):
		if not index is None and index >= 0:
			self.order = index
			self.save()
			
	def remove(self):
		if self.active:
			self.active = False
			self.published = False
			self.title = ''
			self.subtitle = ''
			self.description = ''
			self.order = 0
			self.created_timestamp = None
			self.save()
			
	def reactive(self):
		if not self.active:
			self.active = True
			self.published = False
			self.title = ''
			self.subtitle = ''
			self.description = ''
			self.order = 0
			self.created_timestamp = datetime.now()
			self.save()