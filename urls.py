from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^dotdorset/', include('dotdorset.foo.urls')),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
