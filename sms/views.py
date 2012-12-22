import datetime, logging, time, base64, string, csv, re

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test 
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.simple import direct_to_template
from django.conf import settings

from userena.decorators import secure_required

from forms import SmsForm, MessagingForm, SignupFormOnePage 
from models import Project, Membership, Message, UserDetail
from SmsSender import SmsSender
from MessageGenerator import MessageGenerator

logger = logging.getLogger(__name__)

DATETIME_FORMAT="%m/%d/%Y %H:%M"
TIME_FORMAT="%H:%M"

@login_required
@user_passes_test(lambda u: u.is_staff)
def sms(request):
   if request.method == 'POST': 
      form = SmsForm(request.POST)
      if form.is_valid():
         result = SmsSender().send(form.cleaned_data["phone_number"], form.cleaned_data['message'])
         return HttpResponseRedirect('/') 
   else:
      form = SmsForm() 

   return render_to_response('sms/sms.html',
                             {'form': form },
                             context_instance=RequestContext(request))
       
@login_required
def messaging_select(request, username):
   user = get_object_or_404(User, username__iexact=username)
   if request.method == 'POST':
      form = MessagingForm(request.POST)
      if form.is_valid():
         save_memberships_from_form(user, form)
         return HttpResponseRedirect('/accounts/%s/' % username)
   else:
      user_details = get_user_details(user)
      initial_dict={'user': user_details.user.id,
                    'no_messages': user_details.no_messages}
      form = MessagingForm(initial=initial_dict)
    
   return render_to_response('userena/messaging_form.html',
                             {'form': form },
                             context_instance=RequestContext(request))


#@secure_required
def one_page_signup(request, signup_form=SignupFormOnePage,
           template_name='userena/signup.html'):
   form = SignupFormOnePage(initial = {'smartphone' : True })
   if request.method == 'POST':
      form = signup_form(request.POST, request.FILES)
      if form.is_valid():
         user = form.save()
         redirect_to = settings.SIGNUP_SUCCESSFUL_URL
         # A new signed user should logout the old one.
         if request.user.is_authenticated():
            logout(request)
         return redirect(redirect_to)

   extra_context = dict()
   extra_context['form'] = form
   return direct_to_template(request,
                             template_name,
                             extra_context=extra_context)


# Utility functions

def get_user_details(user):
   user_details_list = UserDetail.objects.filter(user = user.id)
   if len(user_details_list) == 0:
      user_details = UserDetail()
      user_details.user = user
      user_details.smartphone = True
      user_details.no_messages = False
      user_details.save()
      return user_details
   else:
      return user_details_list[0]

def save_memberships_from_form(user, form):
   user_details_list = UserDetail.objects.filter(user = user.id)
   if (len(user_details_list) > 0):
      user_details = user_details_list[0]
   else:
      user_details = UserDetail()
   user_details.no_messages = form.cleaned_data['no_messages']
   user_details.save()
   return

def clean_datetime(datetime_obj):
   if (datetime_obj is None):
      return datetime.datetime.now()
   return datetime_obj
      
def clean_time(time_obj):
   if (time_obj is None):
      now = datetime.datetime.now()
      return datetime.time(now.hour, now.minute)
   return time_obj

def clean_boolean(bool_obj):
   if (bool_obj is None):
      return False
   else:
      return True
      
def clean_integer(int_obj):
   if (int_obj is None):
      return 0
   else:
      return int_obj
      
def formatted_datetime():
   return format_datetime(datetime.datetime.now())

def format_datetime(datetime_obj):
   return datetime_obj.strftime(DATETIME_FORMAT)

def format_time(datetime_obj):
   return datetime_obj.strftime(TIME_FORMAT)

def formatted_time(time_string):
   time_obj = datetime.datetime.strptime(time_string, TIME_FORMAT)
   return datetime.time(time_obj.hour, time_obj.minute)



