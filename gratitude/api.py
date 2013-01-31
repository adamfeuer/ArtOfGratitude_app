from django.contrib.auth.models import User
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

class UserAuthorization(Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(username__exact=request.user.username)
        return object_list.none()

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        list_allowed_methods = ['get']
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        authentication = SessionAuthentication()
        authorization = UserAuthorization()

    def obj_create(self, bundle, request=None, **kwargs):
        return super(UserResource, self).obj_create(bundle, request, user=request.user)

