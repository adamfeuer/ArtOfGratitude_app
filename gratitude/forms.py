from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.utils.translation import ugettext_lazy as _

from userena.forms import SignupFormOnlyEmail

from gratitude.gratitude.models import UserDetail

PROFILE_PLACEHOLDER = 'I am grateful for...'

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
    
class EmailForm(forms.Form):
   message = forms.CharField(max_length=160,widget=forms.Textarea)
   email_address = forms.CharField()

class MessagingForm(forms.Form):
   user_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
   no_messages = forms.BooleanField(required=False, label=_('Do not send me any more emails'), help_text='If you want to stop getting email messages from us, check this box.')

class ProfileForm(forms.Form):
   entry0 = forms.CharField(required=False,max_length=5000,widget=forms.TextInput(attrs={'placeholder':PROFILE_PLACEHOLDER, 'autofocus':'autofocus', 'tabindex': 1}))
   entry1 = forms.CharField(required=False,max_length=5000,widget=forms.TextInput(attrs={'placeholder':PROFILE_PLACEHOLDER, 'tabindex': 2}))
   entry2 = forms.CharField(required=False,max_length=5000,widget=forms.TextInput(attrs={'placeholder':PROFILE_PLACEHOLDER, 'tabindex': 3}))

class SignupFormOnePage(SignupFormOnlyEmail):
   first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder':_('First name')}))
   last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder':_('Last name')}))
   email = forms.EmailField(widget=forms.TextInput(attrs={'class':'required', 'placeholder':_('Email'), 'maxlength':75}), label=_('Email'))
   password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'required', 'placeholder':_('Password')}, render_value=False), label=_('Create password'))
   password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'required', 'placeholder':_('Repeat password')}, render_value=False), label=_('Repeat password'))
   def __init__(self, *args, **kwargs):
      super(SignupFormOnlyEmail, self).__init__(*args, **kwargs)
      del self.fields['password2']
      self.fields.keyOrder = [
            'first_name', 'last_name',
            'email',
            'password1',
            ]

   def save(self):
      """ Saves the user details then calls the base class."""
      user =  super(SignupFormOnePage, self).save()
      userDetail = UserDetail()
      userDetail.user = user
      userDetail.save()
      return user

   def clean(self):
      "Overrride base class to prevent checking that password1 and password2 match, because we don't use password2"
      return self.cleaned_data

class VerificationForm(forms.Form):
   entry0 = forms.CharField(required=False,max_length=5000,widget=forms.TextInput(attrs={'placeholder':PROFILE_PLACEHOLDER, 'autofocus':'autofocus', 'tabindex': 1}))
   entry1 = forms.CharField(required=False,max_length=5000,widget=forms.TextInput(attrs={'placeholder':PROFILE_PLACEHOLDER, 'tabindex': 2}))
   entry2 = forms.CharField(required=False,max_length=5000,widget=forms.TextInput(attrs={'placeholder':PROFILE_PLACEHOLDER, 'tabindex': 3}))
   def __init__(self, *args, **kwargs):
      super(forms.Form, self).__init__(*args, **kwargs)
      self.fields.keyOrder = [
            'entry0',
            'entry1',
            'entry2'
            'activationKey',
            ]

