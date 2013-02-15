from django.conf import settings

from userena.managers import UserenaManager, ASSIGNED_PERMISSIONS
from userena.utils import get_profile_model
from userena.models import UserenaSignup

from models import UserDetail
from guardian.shortcuts import assign

class GratitudeManager(UserenaManager):

   def create_profile_and_userdetail(self, user):
      userDetail = UserDetail()
      userDetail.user = user
      userDetail.save()
      userena_profile = UserenaSignup.objects.create_userena_profile(user)

      # All users have an empty profile
      profile_model = get_profile_model()
      try:
         new_profile = user.get_profile()
      except profile_model.DoesNotExist:
         new_profile = profile_model(user=user)
         new_profile.save(using=self._db)

      # Give permissions to view and change profile
      for perm in ASSIGNED_PERMISSIONS['profile']:
         assign(perm[0], user, new_profile)

      # Give permissions to view and change itself
      for perm in ASSIGNED_PERMISSIONS['user']:
         assign(perm[0], user, user)

      if settings.USERENA_ACTIVATION_REQUIRED:
         userena_profile.send_activation_email()

      return user

   def fix_profile_and_userdetail(self, user):
      userDetail = UserDetail()
      userDetail.user = user
      userDetail.save()

      # All users have an empty profile
      profile_model = get_profile_model()
      try:
         new_profile = user.get_profile()
      except profile_model.DoesNotExist:
         new_profile = profile_model(user=user)
         new_profile.save(using=self._db)

      # Give permissions to view and change profile
      for perm in ASSIGNED_PERMISSIONS['profile']:
         assign(perm[0], user, new_profile)

      # Give permissions to view and change itself
      for perm in ASSIGNED_PERMISSIONS['user']:
         assign(perm[0], user, user)

      return user

