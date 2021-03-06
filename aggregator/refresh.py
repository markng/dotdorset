#! /usr/bin/env python

import sys
import os

def setup_environment():
	pathname = os.path.dirname(sys.argv[0])
	sys.path.append(os.path.abspath(pathname))
	sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
	# setup Django environment
	import settings # your settings module
	from django.core import management
	management.setup_environ(settings)

setup_environment()

from aggregator.models import Feed, FeedItem

feeds = Feed.objects.select_related().all()

for	feed in feeds:
  try:
    refresh = feed.refresh()    
  except Exception, e:
    try:
      print feed.url + ' failed ' + type(e)
    except Exception, e:
      pass
  else:
    try:
      print refresh[0].__unicode__()+' '+refresh[1]
    except Exception, e:
      pass
    

