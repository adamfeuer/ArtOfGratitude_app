from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django_extensions.db.fields.encrypted import EncryptedCharField

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
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()

class UserDetail(models.Model):
   user = models.ForeignKey(User)
   no_messages = models.BooleanField(default=False)
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   
   def __unicode__(self):
      return "'%s': '%s'" % (self.user, self.no_messages)

