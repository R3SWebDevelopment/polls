from django.forms import ModelForm
from django import forms
from models import Album , Image
from r3s_cms.lib.utils import setForm , reorder_fields , required_fields


class AlbumForm(forms.ModelForm):
	class Meta:
		model = Album
		exclude = []
	
	def __init__(self , *args , **kwargs):
		super(AlbumForm, self).__init__(*args, **kwargs)
		instance = kwargs.get('instance') or None
		self.fields = setForm(self.fields)
		if instance:
			self.fields = reorder_fields(self.fields , ['title' , 'subtitle' , 'description'])
			self.fields = required_fields(self.fields , ['title'])
		else:
			self.fields = reorder_fields(self.fields , ['title' , 'subtitle' , 'description'])
			self.fields = required_fields(self.fields , ['title'])
	
	def save(self, commit=True):
		instance = super(AlbumForm, self).save(commit=commit)
		return instance

class ImageForm(forms.ModelForm):
	class Meta:
		model = Album
		exclude = ['slug' , 'created_timestamp']
