from django.http import HttpResponse
from dotdorset.aggregator.models import *
from dotdorset.settings import GOOGLE_MAPS_API_KEYS
from django.template import Template
from django.template.loader import render_to_string
import pprint

def index(request):
  """index view"""
  totemplate = {}
  totemplate['blogitems'] = FeedItem.objects.filter(feed__category__name='Blogs').order_by('-pub_date')[0:5]
  totemplate['twitteritems'] = FeedItem.objects.filter(feed__category__name='Twitter').order_by('-pub_date')[0:15]
  totemplate['mlitems'] = FeedItem.objects.filter(feed__category__name='Mailing List').order_by('-pub_date')[0:5]
  totemplate['jobitems'] = FeedItem.objects.filter(feed__category__name='Jobs').order_by('-pub_date')[0:2]
  totemplate['bookmarkitems'] = FeedItem.objects.filter(feed__category__name='Bookmarks').order_by('-pub_date')[0:20]
  totemplate['eventitems'] = FeedItem.objects.filter(feed__category__name='Events').order_by('-pub_date')[0:2]
  totemplate['map_api_key'] = GOOGLE_MAPS_API_KEYS[request.META['SERVER_NAME']]
  totemplate['keys'] = GOOGLE_MAPS_API_KEYS
  rendered = render_to_string('aggregator_index.html', totemplate)
  return HttpResponse(rendered)
