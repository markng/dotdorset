from django.http import HttpResponse
from dotdorset.aggregator.models import *
from django.template import Template
from django.template.loader import render_to_string
import pprint

def index(request):
  """index view"""
  dictionary = {}
  blogitems = FeedItem.objects.filter(feed__category__name='Blogs').order_by('-pub_date')[0:5]
  twitteritems = FeedItem.objects.filter(feed__category__name='Twitter').order_by('-pub_date')[0:15]
  mlitems = FeedItem.objects.filter(feed__category__name='Mailing List').order_by('-pub_date')[0:5]
  jobitems = FeedItem.objects.filter(feed__category__name='Jobs').order_by('-pub_date')[0:3]
  bookmarkitems = FeedItem.objects.filter(feed__category__name='Bookmarks').order_by('-pub_date')[0:20]
  
  rendered = render_to_string('index.html', {'blogitems': blogitems, 'twitteritems': twitteritems, 'mlitems': mlitems, 'jobitems': jobitems, 'bookmarkitems': bookmarkitems})
  return HttpResponse(rendered)
