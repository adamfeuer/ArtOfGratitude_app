import logging, sys, datetime
from django.contrib.auth.models import User
from django.conf import settings

from userena.models import UserenaSignup

from models import Gratitude, UserDetail
from forms import ProfileForm

logger = logging.getLogger(__name__)

class EntryUtils:
   def __init__(self):
      pass

   def getUsersWhoCanBeEmailed(self):
      # filter out Anonymous users and those who are unsubscribed
      return User.objects.all().order_by('email').filter(id__gt = 0).filter(is_active__exact=True).filter(userdetail__no_messages__exact = False)

   def getUsersWhoHaveNotActivated(self):
      return User.objects.all().order_by('email').filter(id__gt = 0).filter(is_active__exact=False).filter(userdetail__no_messages__exact = False)

   def getActivationKey(self, user):
      return UserenaSignup.objects.all().filter(user_id__exact=user.id)[0].activation_key

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
      today = datetime.datetime.now()
      activationDatetime = UserDetail.get_activation_datetime(user)
      delta = today - activationDatetime
      dayNumber = delta.days + 1
      return dayNumber

   def getUser(self, userid):
      return User.objects.filter(id__exact=userid)[0]

