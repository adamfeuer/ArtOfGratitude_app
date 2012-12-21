from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^$', 'sms.views.sms'),  
    url(r'^sms$', 'sms.views.sms', name="sms"),
)
