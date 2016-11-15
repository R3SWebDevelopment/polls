#from django.forms import ModelForm
from django import forms
from models import InventarioTalento , MapeoSituacional , AnalisisDesempegno , PreCoaching , SessionOne , SessionTwo , SessionThree , SessionFour , SessionFive , SessionSix , AnalisisAvances , ReporteFinalCoaching

class InventarioTalentoForm(forms.ModelForm):
	name = forms.CharField(required = False)
	position = forms.CharField(required = False)
	years = forms.CharField(required = False)
	months = forms.CharField(required = False)
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)

	class Meta:
		model = InventarioTalento
		fields = ['generalComments']
		
		
	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
#		instance = super(InventarioTalentoForm, self).save(commit=False, *args, **kwargs)
		instance = super(InventarioTalentoForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			name = cleanedData.get('name') or None
			position = cleanedData.get('position') or None
			years = cleanedData.get('years') or None
			months = cleanedData.get('months') or None
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
					elif source and source.upper() == 'TALENTOS':
						if action and action.upper() == 'ADD':
							if name and position and years and months:
								added = instance.addTalento(name = name , position = position , years = years , months = months)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeTalento(id = instanceId)
							if removed:
								saved = True
				except:
					pass
		return instance , saved

class MapeoSituacionalForm(forms.ModelForm):
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)

	class Meta:
		model = MapeoSituacional
		fields = ['question_1' , 'question_2' , 'question_3' , 'question_4' , 'generalComments']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(MapeoSituacionalForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
				except:
					pass
		return instance , saved

class AnalisisDesempegnoForm(forms.ModelForm):
	ad_eic_name = forms.CharField(required = False)
	ad_eic_performance = forms.CharField(required = False)
	ad_eic_actitute = forms.CharField(required = False)
	ad_sc_name = forms.CharField(required = False)
	ad_sc_performance = forms.CharField(required = False)
	ad_sc_actitute = forms.CharField(required = False)
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)

	class Meta:
		model = AnalisisDesempegno
		fields = ['generalComments']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(AnalisisDesempegnoForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			ad_eic_name = cleanedData.get('ad_eic_name') or None
			ad_eic_performance = cleanedData.get('ad_eic_performance') or None
			ad_eic_actitute = cleanedData.get('ad_eic_actitute') or None
			ad_sc_name = cleanedData.get('ad_sc_name') or None
			ad_sc_performance = cleanedData.get('ad_sc_performance') or False
			if ad_sc_performance and ad_sc_performance.strip():
				ad_sc_performance = True
			ad_sc_actitute = cleanedData.get('ad_sc_actitute') or False
			if ad_sc_actitute and ad_sc_actitute.strip():
				ad_sc_actitute = True
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
					elif source and source.upper() == 'COLABORADORES':
						if action and action.upper() == 'ADD':
							if ad_eic_name and ad_eic_performance and ad_eic_actitute:
								added = instance.addTalento(name = ad_eic_name , performance = ad_eic_performance , actitute = ad_eic_actitute)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeTalento(id = instanceId)
							if removed:
								saved = True
					elif source and source.upper() == 'COACHEES':
						if action and action.upper() == 'ADD':
							if ad_sc_name:
								added = instance.addCocheeSelection(name = ad_sc_name , performance = ad_sc_performance , actitute = ad_sc_actitute)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeCocheeSelection(id = instanceId)
							if removed:
								saved = True
				except:
					pass
		return instance , saved

class PreCoachingForm(forms.ModelForm):
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)

	class Meta:
		model = PreCoaching
		fields = ['target' , 'stronghold_1' , 'stronghold_2' , 'stronghold_3' , 'opportunity_1' , 'opportunity_2' , 'opportunity_3' , 'recommendation_1' , 'recommendation_2' , 'recommendation_3' , 'session_1' , 'session_2' , 'session_3' , 'session_4' , 'session_5' , 'session_6' , 'place' , 'time' , 'generalComments']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(PreCoachingForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
				except:
					pass
		return instance , saved

class SessionOneForm(forms.ModelForm):
	so_ri_aspect = forms.CharField(required = False)
	so_ri_description = forms.CharField(required = False)
	so_ri_evidence = forms.CharField(required = False)
	so_ao_area = forms.CharField(required = False)
	so_ao_description = forms.CharField(required = False)
	so_ao_evidence = forms.CharField(required = False)
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)

	class Meta:
		model = SessionOne
		fields = ['expectation' , 'comments' , 'targets']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(SessionOneForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			so_ri_aspect = cleanedData.get('so_ri_aspect') or None
			so_ri_description = cleanedData.get('so_ri_description') or None
			so_ri_evidence = cleanedData.get('so_ri_evidence') or None
			so_ao_area = cleanedData.get('so_ao_area') or None
			so_ao_description = cleanedData.get('so_ao_description') or None
			so_ao_evidence = cleanedData.get('so_ao_evidence') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
					elif source and source.upper() == 'FEEDBACK':
						if action and action.upper() == 'ADD':
							if so_ri_aspect and so_ri_description and so_ri_evidence:
								added = instance.addFeedback(aspect = so_ri_aspect , description = so_ri_description , evidence = so_ri_evidence)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeFeedback(id = instanceId)
							if removed:
								saved = True
					elif source and source.upper() == 'OPPORTUNITIES':
						if action and action.upper() == 'ADD':
							if so_ao_area and so_ao_description and so_ao_evidence:
								added = instance.addOpportunity(area = so_ao_area , description = so_ao_description , evidence = so_ao_evidence)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeOpportunity(id = instanceId)
							if removed:
								saved = True
				except:
					pass
		return instance , saved

class SessionTwoForm(forms.ModelForm):
	st_io_need = forms.CharField(required = False)
	st_io_description = forms.CharField(required = False)
	st_it_resource = forms.CharField(required = False)
	st_it_habit = forms.CharField(required = False)
	st_it_actitude = forms.CharField(required = False)
	st_it_learning = forms.CharField(required = False)
	st_it_description = forms.CharField(required = False)
	st_ap_skills = forms.CharField(required = False)
	st_ap_technique = forms.CharField(required = False)
	st_ap_interpersonal = forms.CharField(required = False)
	st_ap_description = forms.CharField(required = False)
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)

	class Meta:
		model = SessionTwo
		fields = ['generalComments']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(SessionTwoForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			st_io_need = cleanedData.get('st_io_need') or None
			st_io_description = cleanedData.get('st_io_description') or None
			st_it_resource = cleanedData.get('st_it_resource') or None
			st_it_habit = cleanedData.get('st_it_habit') or False
			if st_it_habit and st_it_habit.strip():
				st_it_habit = True
			st_it_actitude = cleanedData.get('st_it_actitude') or False
			if st_it_actitude and st_it_actitude.strip():
				st_it_actitude = True
			st_it_learning = cleanedData.get('st_it_learning') or False
			if st_it_learning and st_it_learning.strip():
				st_it_learning = True
			st_it_description = cleanedData.get('st_it_description') or None
			st_ap_skills = cleanedData.get('st_ap_skills') or None
			st_ap_technique = cleanedData.get('st_ap_technique') or False
			if st_ap_technique and st_ap_technique.strip():
				st_ap_technique = True
			st_ap_interpersonal = cleanedData.get('st_ap_interpersonal') or False
			if st_ap_interpersonal and st_ap_interpersonal.strip():
				st_ap_interpersonal = True
			st_ap_description = cleanedData.get('st_ap_description') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
					elif source and source.upper() == 'IMPROVEMENT-ONE':
						if action and action.upper() == 'ADD':
							if st_io_need and st_io_description:
								added = instance.addImprovementOne(need = st_io_need , description = st_io_description)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeImprovementOne(id = instanceId)
							if removed:
								saved = True
					elif source and source.upper() == 'IMPROVEMENT-TWO':
						if action and action.upper() == 'ADD':
							if st_it_resource and st_it_description:
								added = instance.addImprovementTwo(resource = st_it_resource , habit = st_it_habit , actitude = st_it_actitude , learning = st_it_learning , description = st_it_description)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeImprovementTwo(id = instanceId)
							if removed:
								saved = True
					elif source and source.upper() == 'ACTION-PLAN':
						if action and action.upper() == 'ADD':
							if st_ap_skills and st_ap_description:
								added = instance.addActionPlan(skills = st_ap_skills , technique = st_ap_technique , interpersonal = st_ap_interpersonal , description = st_ap_description)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeActionPlan(id = instanceId)
							if removed:
								saved = True
				except:
					pass
		return instance , saved

class SessionThreeForm(forms.ModelForm):
	st_action = forms.CharField(required = False)
	st_description = forms.CharField(required = False)
	st_code = forms.CharField(required = False)
	st_expectedResult = forms.CharField(required = False)
	st_startDate = forms.CharField(required = False)
	st_timing = forms.CharField(required = False)
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)

	class Meta:
		model = SessionThree
		fields = ['generalComments']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(SessionThreeForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			st_action = cleanedData.get('st_action') or None
			st_description = cleanedData.get('st_description') or None
			st_code = cleanedData.get('st_code') or None
			st_expectedResult = cleanedData.get('st_expectedResult') or None
			st_startDate = cleanedData.get('st_startDate') or None
			st_timing = cleanedData.get('st_timing') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
					elif source and source.upper() == 'ACTION':
						if action and action.upper() == 'ADD':
							if st_action and st_description and st_code and st_expectedResult and st_startDate and st_timing:
								added = instance.addAction(action = st_action , description = st_description , code = st_code , expectedResult = st_expectedResult , startDate = st_startDate , timing = st_timing)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeAction(id = instanceId)
							if removed:
								saved = True
				except:
					pass
		return instance , saved

class SessionFourForm(forms.ModelForm):
	sf_performance = forms.CharField(required = False)
	sf_result = forms.CharField(required = False)
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)

	class Meta:
		model = SessionFour
		fields = ['delegated_task' , 'task_impact' , 'first_instruction' , 'second_instruction' , 'third_instruction' , 'benefit' , 'next_task' , 'comments']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(SessionFourForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			sf_performance = cleanedData.get('sf_performance') or None
			sf_result = cleanedData.get('sf_result') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
					elif source and source.upper() == 'PERFORMANCE':
						if action and action.upper() == 'ADD':
							if sf_performance and sf_result:
								added = instance.addPerformance(performance = sf_performance , result = sf_result)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removePerformance(id = instanceId)
							if removed:
								saved = True
				except:
					pass
		return instance , saved

class SessionFiveForm(forms.ModelForm):
	sf_performance = forms.CharField(required = False)
	sf_result = forms.CharField(required = False)
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)

	class Meta:
		model = SessionFive
		fields = ['delegated_task' , 'task_impact' , 'first_instruction' , 'second_instruction' , 'third_instruction' , 'benefit' , 'next_task' , 'comments']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(SessionFiveForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			sf_performance = cleanedData.get('sf_performance') or None
			sf_result = cleanedData.get('sf_result') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
					elif source and source.upper() == 'PERFORMANCE':
						if action and action.upper() == 'ADD':
							if sf_performance and sf_result:
								added = instance.addPerformance(performance = sf_performance , result = sf_result)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removePerformance(id = instanceId)
							if removed:
								saved = True
				except:
					pass
		return instance , saved

class SessionSixForm(forms.ModelForm):
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)
	class Meta:
		model = SessionSix
		fields = ['positive_aspect_1' , 'positive_aspect_2' , 'positive_aspect_3' , 'oportunity_1' , 'oportunity_2' , 'oportunity_3' , 'alternative_1' , 'alternative_2' , 'alternative_3' , 'next_step' , 'renovation_dates' , 'comments']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(SessionSixForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
				except:
					pass
		return instance , saved

class AnalisisAvancesForm(forms.ModelForm):
	aa_description = forms.CharField(required = False)
	aa_evidence = forms.CharField(required = False)
	aa_indicator = forms.CharField(required = False)
	aa_result = forms.CharField(required = False)
	aa_finished = forms.CharField(required = False)
	aa_comments = forms.CharField(required = False)
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)
	class Meta:
		model = AnalisisAvances
		fields = []


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(AnalisisAvancesForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			aa_description = cleanedData.get('aa_description') or None
			aa_evidence = cleanedData.get('aa_evidence') or None
			aa_indicator = cleanedData.get('aa_indicator') or None
			aa_result = cleanedData.get('aa_result') or None
			aa_finished = cleanedData.get('aa_finished') or False
			aa_comments = cleanedData.get('aa_comments') or None
			
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
					elif source and source.upper() == 'TASK':
						if action and action.upper() == 'ADD':
							if aa_description and aa_evidence and aa_indicator and aa_result and aa_comments:
								added = instance.addTask(description = aa_description , evidence = aa_evidence , indicator = aa_indicator , result = aa_result , finished = aa_finished , comments = aa_comments)
								if added:
									saved = True
						if action and action.upper() == 'REMOVE' and instanceId:
							removed = instance.removeTask(id = instanceId)
							if removed:
								saved = True
				except:
					pass
		return instance , saved

class ReporteFinalCoachingForm(forms.ModelForm):
	instanceId = forms.CharField(required = False)
	action = forms.CharField(required = False)
	source = forms.CharField(required = False)
	class Meta:
		model = ReporteFinalCoaching
		fields = ['initial_situation' , 'goal' , 'final_status' , 'main_change' , 'main_difficulty' , 'conclution']


	def save(self, commit=False, force_insert=False, force_update=False, *args, **kwargs):
		instance = super(ReporteFinalCoachingForm, self).save(commit=False)
		if instance:
			saved = False
			cleanedData = self.cleaned_data
			instanceId = cleanedData.get('instanceId') or None
			action = cleanedData.get('action') or None
			source = cleanedData.get('source') or None
			if instance.isSaveEnabled and instance.canBeSaved:
				try:
					if source and source == 'GENERAL':
						if action and action.upper() == 'UPDATE':
							instance.save()
							saved = True
							instance.setUpdatedTimestamp(now = True)
				except:
					pass
		return instance , saved
