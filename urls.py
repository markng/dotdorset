from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dotdorset.aggregator.feed import FullFeed, CategoryFeed
feeds = {
  'categories': CategoryFeed,
  'all': FullFeed
}
admin.autodiscover()
urlpatterns = patterns('',
    (r'^$', 'dotdorset.aggregator.views.index'),
    (r'^join/$', 'dotdorset.join.views.index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/mng/Documents/projects/django/dotdorset/css'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/mng/Documents/projects/django/dotdorset/images'}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/mng/Documents/projects/django/dotdorset/js'}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += staticfiles_urlpatterns()
