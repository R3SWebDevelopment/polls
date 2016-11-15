from django import template

register = template.Library()

@register.simple_tag
def dashboad_business_label():
	return "SB AdminS"