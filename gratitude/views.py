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
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import logout as Signout
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.utils.translation import ugettext as _

from userena.decorators import secure_required
from userena.models import UserenaSignup
from userena.views import ExtraContextTemplateView, signin as userena_signin
from userena import settings as userena_settings
from userena import signals as userena_signals
from userena.managers import UserenaManager
from userena.forms import AuthenticationForm
from userena.utils import signin_redirect

from forms import EmailForm, MessagingForm, SignupFormOnePage, ProfileForm, RememberMeAuthenticationForm
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
         form.save()
         if userena_settings.USERENA_USE_MESSAGES:
             messages.success(request, _('Your profile has been updated.'), fail_silently=True)
      return HttpResponseRedirect(reverse('userena_profile_detail', args=(username,)))
   else:
      user_details = get_user_details(user)
      initial_dict={'user_id': user.id,
                    'no_messages': user_details.no_messages}
      form = MessagingForm(initial=initial_dict)
    
   return render_to_response('userena/messaging_form.html',
                             {'form': form },
                             context_instance=RequestContext(request))


# Todo: needs to not have csrf_exempt
@csrf_exempt
@secure_required
def one_page_signup(request, signup_form=SignupFormOnePage,
           template_name='gratitude/signup.html'):
   form = SignupFormOnePage(initial = {})
   if request.method == 'POST':
      form = signup_form(request.POST)
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
   
@secure_required
def social_verification(request):
   user = request.user
   user.is_active = False
   user.save()
   userenaProfile = UserenaSignup.objects.create_userena_profile(user)
   userenaProfile.send_activation_email()
   redirect_to = settings.SIGNUP_SUCCESSFUL_URL
   if request.user.is_authenticated():
      logout(request)
   return redirect(redirect_to)

@secure_required
def signin(request, auth_form=RememberMeAuthenticationForm,
           template_name='gratitude/signin.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           redirect_signin_function=signin_redirect, extra_context=None):
   return userena_signin(request, auth_form, template_name, redirect_field_name, redirect_signin_function, extra_context)

@login_required
@csrf_exempt
def profile(request, username, profile_form=ProfileForm,
           template_name='gratitude/profile.html'):
   user = get_object_or_404(User, username__iexact=username)
   if (user.username != request.user.username):
      return redirect_to_login(request)
   return profile_simple(request, profile_form, template_name)

@login_required
def profile_simple(request, profile_form=ProfileForm,
      template_name='gratitude/profile.html'):
   if (request.user is None):
      return redirect_to_login(request)
   user = request.user
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
   extra_context['gratitudes_length'] = get_gratitudes_length(gratitudes)
   extra_context['form_fields'] = EntryUtils().getFormFields(user)
   return render_to_response(template_name,
                             extra_context,
                             context_instance=RequestContext(request))

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

@csrf_exempt
def activate(request, activation_key,
             template_name='userena/activate_fail.html',
             extra_context=None):
   """
   Activate a user with an activation key.
   """
   user = UserenaSignup.objects.activate_user(activation_key)
   if user:
      # Sign the user in.
      auth_user = authenticate(identification=user.email,
                               check_password=False)
      login(request, auth_user)
      if userena_settings.USERENA_USE_MESSAGES:
          messages.success(request, _('Congratulations -- your Art of Gratitude account is confirmed!'),
                           fail_silently=True)
      if request.method == 'POST':
         form = ProfileForm(request.POST)
         if form.is_valid():
            save_gratitudes(user, form)
      redirect_to = settings.LOGIN_REDIRECT_URL % {'username': user.username }
      return redirect(redirect_to)
   else:
      if not extra_context: extra_context = {}
      return ExtraContextTemplateView.as_view(template_name=template_name,
                                            extra_context=extra_context)(request)


@secure_required
def signout(request, next_page=userena_settings.USERENA_REDIRECT_ON_SIGNOUT,
            template_name='gratitude/signout.html', *args, **kwargs):
    if request.user.is_authenticated() and userena_settings.USERENA_USE_MESSAGES:
        messages.success(request, _('You have been signed out.'), fail_silently=True)
    return Signout(request, next_page, template_name, *args, **kwargs)

@secure_required
def social_auth_backend_error(request):
   messages.error("Oops! Log in with Facebook or sign up using your email below to get started.")
   return one_page_signup(request)

def server_error(request, template_name='500.html'):
    """ 500 error handler.  """
    return render_to_response(template_name,
        context_instance = RequestContext(request)
    )

# Utility functions

def redirect_to_login(request):
   from django.shortcuts import redirect as django_redirect
   return django_redirect('/app/accounts/signin')

def get_gratitudes(user):
   gratitudes = Gratitude.objects.filter(user_id = user.id)
   gratitudeList = []
   if len(gratitudes) > 0:
      group = []
      currentDay = None
      for gratitude in gratitudes:
         gratitudeDay = gratitude.created.date()
         if gratitudeDay != currentDay:
            currentDay = gratitudeDay
            if len(group) > 0:
               gratitudeList.append(group)
            group = []
         group.append(gratitude)
      if len(group) > 0:
         gratitudeList.append(group)
   gratitudeList.reverse()
   return gratitudeList

def get_gratitudes_length(gratitudes):
   count = 0
   for group in gratitudes:
      count += len(group)
   return count


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



