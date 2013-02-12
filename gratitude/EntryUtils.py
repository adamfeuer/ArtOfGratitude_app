import logging, sys, datetime
from django.contrib.auth.models import User
from django.conf import settings

from models import Gratitude
from forms import ProfileForm

logger = logging.getLogger(__name__)

class EntryUtils:
   def __init__(self):
      pass

   def getUsersWhoCanBeEmailed(self):
      # filter out Anonymous users and those who are unsubscribed
      return User.objects.order_by('email').filter(id__gt = 0).filter(is_active__exact=True).filter(userdetail__no_messages__exact = False)

   def getGratitudes(self, user):
      today = datetime.date.today()
      oneDayInFuture = today + datetime.timedelta(days = 1)
      gratitudes = Gratitude.objects.filter(user_id = user.id).filter(created__range=(today, oneDayInFuture))
      return gratitudes

   def numberOfGratitudesNeeded(self, user):
      return settings.GRATITUDES_PER_DAY - len(self.getGratitudes(user))

   def getFormFields(self, user):
      form = ProfileForm(user=user)
      numberOfGratitudesNeeded = self.numberOfGratitudesNeeded(user)
      formFieldsHtml = []
      for index in xrange(0, numberOfGratitudesNeeded):
         formFieldsHtml.append(form['entry%s' % index])
      return formFieldsHtml[:numberOfGratitudesNeeded]

   def getGratitudeDayNumber(self, user):
      today = datetime.date.today()
      oneDayInFuture = today + datetime.timedelta(days = 1)
      gratitudes = Gratitude.objects.filter(user_id = user.id)
      datetimes = [gratitude.created for gratitude in gratitudes]
      dates = [datetime.date(created.year, created.month, created.day) for created in datetimes] 
      dateDict = {}
      for date in dates:
         dateDict["%s"%date] = True
      uniqueDates = dateDict.keys()
      return len(uniqueDates) + 1

