import time, logging, string
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from django.conf import settings
from gratitude.common.util import flavor_is_not_prod

logger = logging.getLogger(__name__)

class EmailStatus:
   OK = True
   ERROR = False
   def __init__(self, status, message):
      self.status = status
      self.message = message

# TO DO: add amazon simple email service in here
class EmailSender:
   def __init__(self):
      pass

   def send(self, emailAddress, message):
      if (flavor_is_not_prod() and emailAddress not in settings.ALLOWED_EMAIL_ADDRESSES): 
         status = "Not sending message because the phone number is not in ALLOWED_EMAIL_ADDRESSES."
         logger.warn(status)
         return EmailStatus(EmailStatus.ERROR, status)
      # setup
      try:
         # try sending
         logger.info("Sent message to %s." % emailAddress)
      except SomeException as e:
         error_message = "'%s'" % e
         logger.error("Email sending error: %s" % error_message)
         return EmailStatus(EmailStatus.ERROR, error_message)
      return EmailStatus(EmailStatus.OK, message.status)

