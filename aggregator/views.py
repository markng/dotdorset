from django.http import HttpResponse
from dotdorset.aggregator.models import *
from django.template import Template
from django.template.loader import render_to_string
import pprint

def index(request):
  """index view"""
  blogitems = FeedItem.objects.filter(feed__category__name='Blogs').order_by('pub_date')
  twitteritems = FeedItem.objects.filter(feed__category__name='Twitter').order_by('pub_date')
  rendered = render_to_string('index.html', {'blogitems': blogitems, 'twitteritems': twitteritems})
  return HttpResponse(rendered)
