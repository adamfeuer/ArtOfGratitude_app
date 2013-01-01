from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib import admin

from gratitude import views as gratitude_views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('userena.urls')),
    url(r'^accounts/(?P<username>[\.\w]+)/messaging/$', 'gratitude.gratitude.views.messaging_select', name='userena_messaging_select'),
    url(r'^signup', 'gratitude.gratitude.views.one_page_signup'),
    url(r'^profile/(?P<username>[\.\w]+)', 'gratitude.gratitude.views.profile'),
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
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),
)
