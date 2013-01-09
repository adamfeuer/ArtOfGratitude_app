import logging, sys, datetime
from django.contrib.auth.models import User

from models import Gratitude
from forms import ProfileForm

logger = logging.getLogger(__name__)

GRATITUDES_PER_DAY = 3

class EntryUtils:
   def __init__(self):
      pass

   def getUsersWhoCanBeEmailed(self):
      # filter out Anonymous users and those who are unsubscribed
      return User.objects.order_by('email').filter(id__gt = 0).filter(userdetail__no_messages__exact = False)

   def getGratitudes(self, user):
      today = datetime.date.today()
      oneDayInFuture = today + datetime.timedelta(days = 1)
      gratitudes = Gratitude.objects.filter(user_id = user.id).filter(created__range=(today, oneDayInFuture))
      #gratitudes = Gratitude.objects.filter(user_id = user.id)
      return gratitudes

   def numberOfGratitudesNeeded(self, user):
      return GRATITUDES_PER_DAY - len(self.getGratitudes(user))

   def getFormFields(self, user):
      form = ProfileForm()
      numberOfGratitudesNeeded = self.numberOfGratitudesNeeded(user)
      formFieldsHtml = []
      for index in xrange(0, numberOfGratitudesNeeded):
         formFieldsHtml.append(form['entry%s' % index])
      return formFieldsHtml[:numberOfGratitudesNeeded]
