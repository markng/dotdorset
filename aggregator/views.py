from django.http import HttpResponse
from dotdorset.aggregator.models import *
from django.template import Template
import pprint

def index(request):
  """index view"""
  categories = Category.objects.all()
  return HttpResponse(pprint.pformat(items))
