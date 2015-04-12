from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'notice.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^enb/', include('enb.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
