import time, logging, string, re
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from django.conf import settings
from django.core.mail import send_mail
from gratitude.common.util import flavor_is_not_prod

logger = logging.getLogger(__name__)

def send_mail(subject, body, fromEmail, toList):
   emailSender = EmailSender()
   emailSender.send(toList, subject, body, fromEmail)

class EmailStatus:
   OK = True
   ERROR = False

   def __init__(self, status, message):
      self.status = status
      self.message = message

   def __unicode__(self):
      return "'%s': '%s %s'" % (self.status, self.message)

class EmailSender:
   def __init__(self):
      pass

   def send(self, toList, subject, body, fromEmail=settings.DEFAULT_FROM_EMAIL):
      toListWithoutPluses = self.removePlusesFromEmails(toList)
      self.statusList = []
      if (flavor_is_not_prod() and not self.emailAddressesAllowed(toListWithoutPluses)):
         return self.emailAddressNotAllowed(toList)
      else:
         try:
            email = EmailMultiAlternatives(subject, "", fromEmail, toList)
            email.attach_alternative(body, 'text/html')
            email.send()
            #print("Sent message to %s." % toList)
            logger.info("Sent message to %s." % toList)
         except Exception as e:
            return self.emailSendingError(toListWithoutPluses, e)
      return EmailStatus(EmailStatus.OK, "")

   def emailAddressesAllowed(self, toList):
      for emailAddress in toList:
         if emailAddress not in settings.ALLOWED_EMAIL_ADDRESSES:
            return False
      return True

   def emailSendingError(self, emailAddress, exception):
      error_message = "'%s'" % exception
      #print("Email sending error: %s" % error_message)
      logger.error("Email sending error (%s): %s" % (emailAddress, error_message))
      return EmailStatus(EmailStatus.ERROR, error_message)

   def emailAddressNotAllowed(self, emailAddresses):
      status = "Not sending email because one of the email addresses in the list %s is not in settings.ALLOWED_EMAIL_ADDRESSES." % (emailAddresses)
      #print(status)
      logger.warn(status)
      return EmailStatus(EmailStatus.ERROR, status)

   def removePlusesFromEmails(self, toList):
      newToList = []
      for emailAddress in toList:
         newToList.append(self.removePluses(emailAddress))
      return newToList

   def removePluses(self, emailAddress):
      newAddress = re.sub('\+.*\@', '@', emailAddress)
      return newAddress

