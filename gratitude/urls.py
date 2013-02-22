from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from tastypie.api import Api
from .api import UserResource, ActionResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ActionResource())

urlpatterns = patterns('',
    url(r'^email$', 'gratitude.gratitude.views.email', name="email"),
    (r'^api/', include(v1_api.urls)),
)
