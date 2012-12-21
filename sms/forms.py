from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.utils.translation import ugettext_lazy as _

from userena.forms import SignupFormOnlyEmail

from sms.models import Project, Membership, UserDetail

def get_datetime_field():
   return StrippingDateTimeField(required=False, widget=forms.TextInput(attrs={'class':'jquery-datetime'}))
    
def get_time_field():
   return StrippingTimeField(required=False, widget=forms.TimeInput(format="%H:%M", attrs={'class':'jquery-time'}))

class StrippingTimeField(forms.TimeField):
   def to_python(self, value):
      return super(StrippingTimeField, self).to_python(value.strip())      
    
class StrippingDateTimeField(forms.DateTimeField):
   def to_python(self, value):
      return super(StrippingDateTimeField, self).to_python(value.strip())      
    
class SmsForm(forms.Form):
   message = forms.CharField(max_length=160,widget=forms.Textarea)
   phone_number = forms.CharField()

class MessagingForm(forms.Form):
   user_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
   no_messages = forms.BooleanField(required=False, label=_('Do not send me any more emails'), help_text='If you want to stop getting email messages from us, check this box.')

class SignupFormOnePage(SignupFormOnlyEmail):
   def __init__(self, *args, **kwargs):
      super(SignupFormOnlyEmail, self).__init__(*args, **kwargs)
      self.fields.keyOrder = [
            'email',
            'password1',
            'password2'
            ]

   def save(self):
      """ Saves the user details then calls the base class."""
      user =  super(SignupFormOnePage, self).save()
      user.save()

      userDetail = UserDetail()
      userDetail.user = user
      userDetail.save()
      return user

