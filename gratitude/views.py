import datetime, logging, time, base64, string, csv, re

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
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

from forms import EmailForm, MessagingForm, SignupFormOnePage, ProfileForm
from models import UserDetail, Gratitude
from EmailSender import EmailSender
from EntryUtils import EntryUtils

logger = logging.getLogger(__name__)

DATETIME_FORMAT="%m/%d/%Y %H:%M"
TIME_FORMAT="%H:%M"

@login_required
@user_passes_test(lambda u: u.is_staff)
def email(request):
   if request.method == 'POST': 
      form = EmailForm(request.POST)
      if form.is_valid():
         result = EmailSender().send(form.cleaned_data["email"], form.cleaned_data['message'])
         return HttpResponseRedirect('/') 
   else:
      form = EmailForm() 

   return render_to_response('email/email.html',
                             {'form': form },
                             context_instance=RequestContext(request))
       
@login_required
def messaging_select(request, username):
   user = get_object_or_404(User, username__iexact=username)
   if request.method == 'POST':
      form = MessagingForm(request.POST)
      if form.is_valid():
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
   form = SignupFormOnePage(initial = {})
   if request.method == 'POST':
      form = signup_form(request.POST, request.FILES)
      if form.is_valid():
         user = form.save()
         user.first_name = form.cleaned_data['first_name']
         user.last_name = form.cleaned_data['last_name']
         user.save()
         redirect_to = settings.SIGNUP_SUCCESSFUL_URL
         # A new signed user should logout the old one.
         if request.user.is_authenticated():
            logout(request)
         return redirect(redirect_to)

   extra_context = {}
   extra_context.update(csrf(request))
   extra_context['form'] = form
   return direct_to_template(request,
                             template_name,
                             extra_context=extra_context)


@login_required
@csrf_exempt
def profile(request, username, profile_form=ProfileForm,
           template_name='gratitude/profile.html'):
   user = get_object_or_404(User, username__iexact=username)
   if request.method == 'POST':
      form = profile_form(request.POST, request.FILES)
      if form.is_valid():
         save_gratitudes(user, form)
   form = ProfileForm(initial = {})
   extra_context = {}
   extra_context.update(csrf(request))
   extra_context['user'] = user 
   gratitudes = get_gratitudes(user)
   extra_context['gratitudes'] = gratitudes
   extra_context['form_fields'] = EntryUtils().getFormFields(user)
   return render_to_response(template_name,
                             extra_context,
                             context_instance=RequestContext(request))

@login_required
@csrf_exempt
def unsubscribe(request, username, template_name='gratitude/unsubscribe.html'):
   user = get_object_or_404(User, username__iexact=username)
   userDetail = get_user_details(user)
   userDetail.no_messages = True
   userDetail.save()
   extra_context = {}
   extra_context['user'] = user 
   return render_to_response(template_name,
                             extra_context,
                             context_instance=RequestContext(request))
# Utility functions

def get_gratitudes(user):
   gratitudes = Gratitude.objects.filter(user_id = user.id)
   return(gratitudes)

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

def save_user_details(user, form):
   user_details_list = UserDetail.objects.filter(user = user.id)
   if (len(user_details_list) > 0):
      user_details = user_details_list[0]
   else:
      user_details = UserDetail()
   user_details.no_messages = form.cleaned_data['no_messages']
   user_details.save()
   return

def save_gratitudes(user, form):
   for entry in ['entry0', 'entry1', 'entry2']:
      cleanEntry = form.cleaned_data[entry].strip()
      if (len(cleanEntry) > 0):
         newGratitudeEntry = Gratitude()
         newGratitudeEntry.user_id = user.id
         newGratitudeEntry.text = cleanEntry
         newGratitudeEntry.save()

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



