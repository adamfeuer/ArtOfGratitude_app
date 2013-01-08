import logging, sys, datetime
from django.contrib.auth.models import User

import cronjobs
from EmailSender import EmailSender, EmailStatus
from EntryUtils import EntryUtils
from models import Gratitude

logger = logging.getLogger(__name__)

@cronjobs.register
def sendMessages():
   entryUtils = EntryUtils()
   users = entryUtils.getUsersWhoCanBeEmailed()
   #User.objects.order_by('email').filter(id__gt = 0)
   print users
   for user in users:
      gratitudes = entryUtils.getGratitudes(user)
      numberOfGratitudesNeeded = entryUtils.numberOfGratitudesNeeded()
      if (numberOfGratitudesNeeded > 0):
         print numberOfGratitudesNeeded
         sendEmail(user, numberOfGratitudesNeeded)

def sendEmail(user, numberOfGratitudesNeeded):
   messageSender = EmailSender()
   subject = getEmailSubjectLine(user)
   body = getEmailBody(user, numberOfGratitudesNeeded)
   print("Sending message %s [%s]: %s %s" % (user.email, user.id, subject, numberOfGratitudesNeeded))
   logger.info("Sending message %s [%s]: %s %s" % (user.email, user.id, subject, numberOfGratitudesNeeded))
   #status = message_sender.send(user.email, message.message)
   #logger.info("Sending message %s: %s" % (user.email, subject)

def getEmailSubjectLine(user):
   return "subject"

def getEmailBody(user, numberOfGratitudesNeeded):
   return "body"

