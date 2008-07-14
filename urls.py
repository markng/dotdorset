from django.conf.urls.defaults import *
from dotdorset.aggregator.feed import FullFeed, CategoryFeed
feeds = {
  'categories': CategoryFeed,
  'all': FullFeed
}

urlpatterns = patterns('',
    # Example:
    # (r'^dotdorset/', include('dotdorset.foo.urls')),
    (r'^$', 'dotdorset.aggregator.views.index'),
    (r'^join/$', 'dotdorset.join.views.index'),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/mng/Documents/projects/django/dotdorset/css'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/mng/Documents/projects/django/dotdorset/images'}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/mng/Documents/projects/django/dotdorset/js'}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
