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
   
class UserProfile(models.Model):
   user_id = EncryptedCharField(max_length=100)
   days_left = models.IntegerField()
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
    
   def __unicode__(self):
      return self.user_id

class Gratitude(models.Model):
   user_id = EncryptedCharField(max_length=100)
   gratitude = models.CharField(max_length=5000)
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()

class Message(models.Model):
   user_id = EncryptedCharField(max_length=100)
   identifier = EncryptedCharField(max_length=100)
   email_address = EncryptedCharField(max_length=200)
   message = EncryptedCharField(max_length=300)
   send_at = models.DateTimeField()
   sent = models.BooleanField()
   sent_status = models.BooleanField()
   sent_error_message = models.CharField(max_length=200)
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   
   def __unicode__(self):
      return "'%s': '%s %s'" % (self.user_id, self.email_address, self.message)
   
class UserDetail(models.Model):
   user = models.ForeignKey(User)
   no_messages = models.BooleanField()
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   
   def __unicode__(self):
      return "'%s': '%s'" % (self.user, self.phone_number)

