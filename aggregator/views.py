from django.http import HttpResponse
from aggregator.models import *
from settings import GOOGLE_MAPS_API_KEYS
from django.template import Template
from django.template.loader import render_to_string
from django.template import RequestContext
import pprint

def index(request):
  """index view"""
  totemplate = {}
  totemplate['blogitems'] = FeedItem.objects.filter(feed__category__name='Blogs').order_by('-pub_date')[0:7]
  totemplate['twitteritems'] = FeedItem.objects.filter(feed__category__name='Twitter').order_by('-pub_date')[0:17]
  totemplate['mlitems'] = FeedItem.objects.filter(feed__category__name='Mailing List').order_by('-pub_date')[0:6]
  totemplate['jobitems'] = FeedItem.objects.filter(feed__category__name='Jobs').order_by('-pub_date')[0:3]
  totemplate['bookmarkitems'] = FeedItem.objects.filter(feed__category__name='Bookmarks').order_by('-pub_date')[0:20]
  totemplate['eventitems'] = FeedItem.objects.filter(feed__category__name='Events').order_by('-pub_date')[0:3]
  context = RequestContext(request, totemplate)
  rendered = render_to_string('aggregator_index.html', context)
  return HttpResponse(rendered)
