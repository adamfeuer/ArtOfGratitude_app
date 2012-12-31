from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    #(r'^$', 'gratitude.views'),  
    url(r'^email$', 'gratitude.gratitude.views.email', name="email"),
)
