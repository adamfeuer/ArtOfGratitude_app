import time, logging, string, re
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from django.conf import settings
from django.core.mail import send_mail
from gratitude.common.util import flavor_is_not_prod

logger = logging.getLogger(__name__)

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

   def send(self, emailAddress, subject, body):
      emailAddressWithoutPluses = self.removePluses(emailAddress)
      if (flavor_is_not_prod() and emailAddressWithoutPluses not in settings.ALLOWED_EMAIL_ADDRESSES): 
         status = "Not sending email because the email address %s (%s) is not in ALLOWED_EMAIL_ADDRESSES." % (emailAddress, emailAddressWithoutPluses)
         logger.warn(status)
         return EmailStatus(EmailStatus.ERROR, status)
      try:
         #send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [emailAddress], fail_silently=False)
         email = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [emailAddress])
         email.attach_alternative(body, 'text/html')
         email.send()
         logger.info("Sent message to %s." % emailAddress)
      except Exception as e:
         error_message = "'%s'" % e
         print("Email sending error: %s" % error_message)
         logger.error("Email sending error: %s" % error_message)
         return EmailStatus(EmailStatus.ERROR, error_message)
      return EmailStatus(EmailStatus.OK, "")

   def removePluses(self, emailAddress):
      newAddress = re.sub('\+.*\@', '@', emailAddress)
      return newAddress

