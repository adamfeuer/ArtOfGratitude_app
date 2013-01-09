import logging, sys, datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

import cronjobs
from EmailSender import EmailSender, EmailStatus
from EntryUtils import EntryUtils
from models import Gratitude
from forms import ProfileForm

logger = logging.getLogger(__name__)

@cronjobs.register
def sendMessages():
   entryUtils = EntryUtils()
   users = entryUtils.getUsersWhoCanBeEmailed()
   for user in users:
      gratitudes = entryUtils.getGratitudes(user)
      numberOfGratitudesNeeded = entryUtils.numberOfGratitudesNeeded(user)
      if (numberOfGratitudesNeeded > 0):
         sendEmail(user, numberOfGratitudesNeeded)

def sendEmail(user, numberOfGratitudesNeeded):
   emailSender = EmailSender()
   subject = getEmailSubjectLine(user)
   body = getEmailBody(user, numberOfGratitudesNeeded)
   print("Sending message %s [%s]: %s %s" % (user.email, user.id, subject, numberOfGratitudesNeeded))
   logger.info("Sending message %s [%s]: %s %s" % (user.email, user.id, subject, numberOfGratitudesNeeded))
   status = emailSender.send(user.email, subject, body)

def getEmailSubjectLine(user):
   subject = render_to_string("gratitude/emails/daily_email_subject.txt",
                              getContext(user))
   subject = ''.join(subject.splitlines())
   return subject

def getEmailBody(user, numberOfGratitudesNeeded):
   body = render_to_string("gratitude/emails/daily_email_body.html",
                              getContext(user))
   return body

def getContext(user):
   context = {'user': user,
              'site': Site.objects.get_current(),
              'settings': settings,
              'form_fields': getFormFields(user)}
   return context

def getFormFields(user):
   form = ProfileForm()
   entryUtils = EntryUtils()
   numberOfGratitudesNeeded = entryUtils.numberOfGratitudesNeeded(user)
   formFieldsHtml = []
   for index in xrange(0, numberOfGratitudesNeeded):
      formFieldsHtml.append(form['entry%s' % index])
   return formFieldsHtml[:numberOfGratitudesNeeded]

