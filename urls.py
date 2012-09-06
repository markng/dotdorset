from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from aggregator.feed import FullFeed, CategoryFeed
feeds = {
  'categories': CategoryFeed,
  'all': FullFeed
}
admin.autodiscover()
urlpatterns = patterns('',
    (r'^$', 'aggregator.views.index'),
    (r'^join/$', 'join.views.index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += staticfiles_urlpatterns()
