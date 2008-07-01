from django.http import HttpResponse
from dotdorset.aggregator.models import *
import pprint

def index(request):
  """index view"""
  categories = Category.objects.all()
  return HttpResponse(pprint.pformat(items))
