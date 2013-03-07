import logging, datetime

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, DateTimeField
from django_extensions.db.fields.encrypted import EncryptedCharField

logger = logging.getLogger(__name__)

class Setting(models.Model):
   name = models.CharField(max_length=200)
   value = models.CharField(max_length=500)
   description = models.CharField(max_length=500)
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
    
   def __unicode__(self):
      return self.name
   
class Gratitude(models.Model):
   user_id = models.CharField(max_length=100)
   text = models.CharField(max_length=5000)
   stashed = models.BooleanField(default=False)
   stash_id = models.CharField(max_length=100, default="")
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   
class UserDetail(models.Model):
   user = models.ForeignKey(User)
   no_messages = models.BooleanField(default=False)
   activated = DateTimeField(null=True)
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   
   def __unicode__(self):
      return "'%s': '%s'" % (self.user, self.no_messages)

   @staticmethod
   def set_activation_datetime(user):
      userDetails = UserDetail.objects.filter(user = user.id)
      if len(userDetails) > 0:
         userDetail = userDetails[0]
      else:
         userDetail = UserDetail()
         userDetail.user = user
      userDetail.activated = datetime.datetime.now()
      userDetail.save()

   @staticmethod
   def get_activation_datetime(user):
      userDetails = UserDetail.objects.filter(user = user.id)
      if len(userDetails) > 0:
         userDetail = userDetails[0]
         return userDetail.activated
      else:
         return None

class Action(models.Model):
   user = models.ForeignKey(User)
   gratitude = models.ForeignKey(Gratitude, null=True)
   action = models.CharField(max_length = 500)
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   SHARE_SITE_FACEBOOK = 'share_site_facebook'
   SHARE_SITE_TWITTER = 'share_site_twitter'
   SHARE_GRATITUDE_FACEBOOK = 'share_gratitude_facebook'
   SHARE_GRATITUDE_TWITTER = 'share_gratitude_twitter'
   SEND_THANKS_FACEBOOK = 'send_thanks_facebook'
   ALLOWED_ACTIONS = [SHARE_SITE_FACEBOOK, SHARE_SITE_TWITTER, SHARE_GRATITUDE_FACEBOOK, SHARE_GRATITUDE_TWITTER, SEND_THANKS_FACEBOOK]
   
   def __unicode__(self):
      return "'%s': '%s'" % (self.user, self.action)
   
   @staticmethod
   def get_action_count_for_user(user, action):
         return Action.objects.all().filter(user_id = user.id).filter(action__exact = action).count()

