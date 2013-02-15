import logging, sys, datetime, os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

import cronjobs
from EmailSender import EmailSender, EmailStatus
from MonitorUtils import MonitorUtils
from EntryUtils import EntryUtils
from Quotes import Quotes
from models import Gratitude
from forms import ProfileForm
from managers import GratitudeManager

logger = logging.getLogger('email_sender')

@cronjobs.register
def sendMessages():
   monitorUtils = MonitorUtils()
   if monitorUtils.isWebserverRunning():  
      timeBeforeSending = datetime.datetime.now()
      count = 0
      entryUtils = EntryUtils()
      users = entryUtils.getUsersWhoCanBeEmailed()
      logger.info("About to send emails, checking %d users." % len(users))
      for user in users:
         gratitudes = entryUtils.getGratitudes(user)
         numberOfGratitudesNeeded = entryUtils.numberOfGratitudesNeeded(user)
         if (numberOfGratitudesNeeded > 0):
            count += 1
            sendEmail(user, numberOfGratitudesNeeded)
      timeAfterSending = datetime.datetime.now()
      interval = timeAfterSending - timeBeforeSending
      logger.info("Sent %d emails in %s" % (count, interval))
   else:
      logger.error("Webserver is not running - not sending emails!")

def sendEmail(user, numberOfGratitudesNeeded):
   emailSender = EmailSender()
   subject = getEmailSubjectLine(user)
   body = getEmailBody(user, numberOfGratitudesNeeded)
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
   context = {'user': user,
              'site': Site.objects.get_current(),
              'site_prefix': settings.SITE_PREFIX,
              'settings': settings,
              'quote_text': quote.text,
              'quote_author': quote.author,
              'gratitudeDayNumber': gratitudeDayNumber,
              'form_fields': entryUtils.getFormFields(user)}
   return context


abspath = lambda *p: os.path.abspath(os.path.join(*p))

@cronjobs.register
def sendMessagesAndFix():
   gratitudeManager = GratitudeManager()
   thisDir = abspath(os.path.dirname(__file__))
   user_ids = map(int, open(os.path.join(thisDir, "idsToFix")).readlines())
   print "attempting to fix user_ids %s" % user_ids
   for user_id in user_ids:
      user = User.objects.filter(id__exact = user_id)[0]
      print "User %s %s <%s>" % (user.first_name, user.last_name, user.email)
      timeBeforeSending = datetime.datetime.now()
      count = 0
      entryUtils = EntryUtils()
      logger.info("About to send email to user %s..." % user.email)
      gratitudes = entryUtils.getGratitudes(user)
      numberOfGratitudesNeeded = entryUtils.numberOfGratitudesNeeded(user)
      if (numberOfGratitudesNeeded > 0):
         count += 1
         gratitudeManager.fix_profile_and_userdetail(user)
         sendEmail(user, numberOfGratitudesNeeded)
      timeAfterSending = datetime.datetime.now()
      interval = timeAfterSending - timeBeforeSending
      print "Sent %d emails in %s" % (count, interval)
      logger.info("Sent %d emails in %s" % (count, interval))
