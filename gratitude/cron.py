import logging, sys, datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

import cronjobs
from EmailSender import EmailSender, EmailStatus
from EntryUtils import EntryUtils
from Quotes import Quotes
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
   status = emailSender.send([user.email], subject, body)

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
   entryUtils = EntryUtils()
   gratitudeDayNumber = entryUtils.getGratitudeDayNumber(user)
   quote = Quotes().getQuote(gratitudeDayNumber)
   print quote
   context = {'user': user,
              'site': Site.objects.get_current(),
              'settings': settings,
              'quote_text': quote.text,
              'quote_author': quote.author,
              'gratitudeDayNumber': gratitudeDayNumber,
              'form_fields': entryUtils.getFormFields(user)}
   return context

