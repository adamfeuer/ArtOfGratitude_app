import logging, sys, datetime
from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand, CommandError

import gratitude
from gratitude.gratitude.EmailSender import EmailSender, EmailStatus
from gratitude.gratitude.Quotes import Quotes

GRATITUDES_PER_DAY = 3

class Command(BaseCommand):
   option_list = BaseCommand.option_list + (
      make_option('--email_body',
          action='store',
          dest='emailBodyTemplate',
          default="gratitude/emails/daily_email_body.html",
          help='path to email body template'),
      ) + (
      make_option('--email_subject',
          action='store',
          dest='emailSubjectTemplate',
          default="gratitude/emails/daily_email_subject.txt",
          help='path to email subject template'),
      ) + (
      make_option('--email_address',
          action='store',
          dest='emailAddress',
          default="",
          help='path to email subject template'),
      ) + (
      make_option('--number_of_gratitudes_needed',
          action='store',
          dest='numberOfGratitudesNeeded',
          default="1",
          help='number of gratitudes needed'),
      ) + (
      make_option('--number_of_gratitudes_entered',
          action='store',
          dest='numberOfGratitudesEntered',
          default="1",
          help='number of gratitudes entered'),
      ) + (
      make_option('--first_name',
          action='store',
          dest='firstName',
          default="",
          help='first name'),
      ) + (
      make_option('--last_name',
          action='store',
          dest='lastName',
          default="",
          help='last name'),
      ) + (
      make_option('--gratitude_day_number',
          action='store',
          dest='gratitudeDayNumber',
          default="1",
          help='gratitude day number'),
      ) + (
      make_option('--username',
          action='store',
          dest='username',
          default="",
          help='username'),
      )
   def handle(self, *args, **options):
      self.numberOfGratitudesNeeded = int(options['numberOfGratitudesNeeded'])
      self.numberOfGratitudesEntered = int(options['numberOfGratitudesEntered'])
      self.emailAddress = options['emailAddress']
      self.emailSubjectTemplate = options['emailSubjectTemplate']
      self.emailBodyTemplate = options['emailBodyTemplate']
      self.firstName = options['firstName']
      self.lastName = options['lastName']
      self.username = options['username']
      self.gratitudeDayNumber = options['gratitudeDayNumber']
      user = self.getUser()
      user.numberOfGratitudesEntered = self.numberOfGratitudesEntered
      user.numberOfGratitudesNeeded = self.numberOfGratitudesNeeded
      self.sendEmail(user, self.numberOfGratitudesNeeded)
      
   def sendEmail(self, user, numberOfGratitudesNeeded):
      emailSender = EmailSender()
      subject = self.getEmailSubjectLine(user)
      body = self.getEmailBody(user, numberOfGratitudesNeeded)
      print("Sending message %s: %s %s" % (user.email, subject, numberOfGratitudesNeeded))
      status = emailSender.send([user.email], subject, body)

   def getEmailSubjectLine(self, user):
      subject = render_to_string(self.emailSubjectTemplate,
                                 self.getContext(user))
      subject = ''.join(subject.splitlines())
      return subject

   def getEmailBody(self, user, numberOfGratitudesNeeded):
      body = render_to_string(self.emailBodyTemplate,
                                 self.getContext(user))
      return body

   def getUser(self):
      user = User()
      user.email = self.emailAddress
      user.first_name = self.firstName
      user.last_name = self.lastName
      user.username = self.username
      return user

   def getContext(self, user):
      quote = Quotes().getQuote(self.gratitudeDayNumber)
      context = {'site': Site.objects.get_current(),
                 'site_prefix': settings.SITE_PREFIX,
                 'user': user,
                 'settings': settings,
                 'quote_text': quote.text,
                 'quote_author': quote.author,
                 'gratitudeDayNumber': self.gratitudeDayNumber,
                 'form_fields': self.getFormFields(user)}
      return context

   def getFormFields(self, user):
      form = gratitude.gratitude.forms.ProfileForm()
      numberOfGratitudesNeeded = user.numberOfGratitudesNeeded
      formFieldsHtml = []
      for index in xrange(0, numberOfGratitudesNeeded):
         formFieldsHtml.append(form['entry%s' % index])
      return formFieldsHtml[:numberOfGratitudesNeeded]

