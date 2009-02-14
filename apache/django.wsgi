import os, sys
sys.path.append('/home/mng')
sys.path.append('/home/mng/dotdorset')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dotdorset.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
