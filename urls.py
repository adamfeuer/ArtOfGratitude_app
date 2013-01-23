from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from adminplus import AdminSitePlus
from django_ses.views import dashboard

from userena import views as userena_views
from gratitude import views as gratitude_views

admin.site = AdminSitePlus()
admin.autodiscover()
admin.site.register_view('django-ses', dashboard, 'Django SES Stats')

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^signout$', 'gratitude.gratitude.views.signout', name='gratitude_signout'),
    (r'^accounts/', include('userena.urls')),
    url(r'^accounts/(?P<username>[\.\w]+)/messaging/$', 'gratitude.gratitude.views.messaging_select', name='userena_messaging_select'),
    url(r'^signup$', 'gratitude.gratitude.views.one_page_signup', name='gratitude_signup'),
    url(r'^signup-verification$', 
         direct_to_template, 
         {'template': 'gratitude/signup_complete.html'}, 
         name='signup-verification'),
    url(r'^profile/(?P<username>[\.\w]+)', 'gratitude.gratitude.views.profile'),
    url(r'^unsubscribe/(?P<username>[\.\w]+)', 'gratitude.gratitude.views.unsubscribe', name='gratitude_unsubscribe'),
    url(r'^$',
        direct_to_template,
        {'template': 'static/home.html'},
        name='home'),
    url(r'^about$',
        direct_to_template,
        {'template': 'static/about.html'},
        name='about'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^gratitude/', include('gratitude.gratitude.urls')),
    url(r'^activate/(?P<activation_key>\w+)/$', 'gratitude.gratitude.views.activate', name='gratitude_activate'),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),
)
