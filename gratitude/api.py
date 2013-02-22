import datetime, logging

from django.contrib.auth.models import User
from django.conf import settings 

from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource, ModelResource

from .models import Action, Gratitude

logger = logging.getLogger(__name__)

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

class ActionLimitReached(Exception):
   """Exception raised when too many actions for one day have been saved"""
   pass

class ActionResource(Resource):
   class Meta:
      resource_name = 'action'
      list_allowed_methods = Action.ALLOWED_ACTIONS
      excludes = []
      authentication = SessionAuthentication()
      authorization = UserAuthorization()

   def obj_create(self, bundle, request=None, **kwargs):
      return super(ActionResource, self).obj_create(bundle, request, user=request.user)

   def obj_get(self, request=None, **kwargs):
      tokens = kwargs['pk'].split('/')
      if len(tokens) == 1:
         method = tokens[0]
         gratitude_id = None 
      else:
         method, gratitude_id = tokens[:2]
      if method in Action.ALLOWED_ACTIONS:
         return self._new_action(request.user, method, gratitude_id)
      else: 
         raise NotImplementedError()

   def _action_limit_reached(self, user):
      now = datetime.datetime.now()
      today = now.date()
      todaysActions = Action.objects.all().filter(user_id = user.id).filter(created__gte = today).count()
      result = False
      if todaysActions > settings.MAX_ACTIONS_PER_DAY:
         result = True
      return result

   def _new_action(self, user, actionText, gratitude_id=None):
      if self._action_limit_reached(user):
         message = "Action limit reached for user %s (id: %s) (%s)" % (user.username, user.id, user.email) 
         logger.warn(message)
         raise ActionLimitReached(message)
      gratitude = None
      if gratitude_id is not None:
         gratitude_id_as_int = int(gratitude_id)
         gratitudes = Gratitude.objects.all().filter(id=gratitude_id_as_int)
         if len(gratitudes) == 1:
            gratitude = gratitudes[0]
      action = Action()
      action.user = user
      action.gratitude = gratitude
      action.action = actionText
      action.save()
      return action

