#from models import Hit
from models import BaysingersHit as Hit

def analytics(view_func):
	def _wrapped_view_func(request , *args , **kwargs):
		Hit.page_visited(request = request)
		return view_func(request , *args , **kwargs)
	return _wrapped_view_func