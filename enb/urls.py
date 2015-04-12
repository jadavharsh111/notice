from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from enb import views

urlpatterns = patterns('',
    url(r'^$',views.start_page.as_view(),name='start_page'),
    url(r'^plan/$',views.plan.as_view(),name='plan'),
    url(r'^main_page/$',views.main_page,name='main_page'),
    url(r'^submit/$',views.submit_page,name='submit'),
    url(r'^tag/([^\s]+)/$', views.tag_page, name='tag_page'),
    url(r'^tag/$', views.tag_cloud_page, name='tag_cloud'),
    url(r'^user/(\w+)/$', views.user_page, name='user_page'),

#session management
url(r'^login/$','django.contrib.auth.views.login', name='login'),
url(r'^logout/$',views.logout_page, name='logout'),
url(r'^register/$', views.register_page, name='register'),
url(r'^success/$', views.RegisterSuccess.as_view(), name='success'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
