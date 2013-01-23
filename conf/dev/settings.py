import os, ConfigParser
from gratitude.settings import *

SURVEYTOOL_CONFIG = os.path.join(os.environ['WORKON_HOME'], 'gratitude', 'gratitude.config')
config = ConfigParser.RawConfigParser()
config.read(SURVEYTOOL_CONFIG)
TWILIO_FROM_PHONE_NUMBER = config.get('Twilio', 'TWILIO_FROM_PHONE_NUMBER')
TWILIO_ACCOUNT = config.get('Twilio', 'TWILIO_ACCOUNT')
TWILIO_TOKEN = config.get('Twilio', 'TWILIO_TOKEN')
DATABASE_HOST = config.get('Database', 'host')
DATABASE_USER = config.get('Database', 'user')
DATABASE_PASSWORD = config.get('Database', 'password')
DATABASE_DB = config.get('Database', 'database')
# AWS settings 
AWS_ACCESS_KEY_ID = config.get('AWS', 'user')
AWS_SECRET_ACCESS_KEY = config.get('AWS', 'password')

SITE='local.artofgratitude.com'
SITE_URL='https://' + SITE
SITE_PREFIX='/app'
BASE_URL = SITE_URL
SITE_ID = 3
FORCE_SCRIPT_NAME = SITE_PREFIX

STATIC_ROOT = 'static'
STATIC_URL = '/app/static/'
LOGFILE_PATH = 'logs/gratitude.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOGFILE_PATH,
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
                'level':'INFO',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': 'logs/django_request.log',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
        'email_sender': {
                'level':'INFO',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': 'logs/email_sender.log',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': { # Stop SQL debug from logging to main logger
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': DATABASE_HOST,
        'NAME': DATABASE_DB,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        }
}

# Key Czar and django-extensions
ENCRYPTED_FIELD_KEYS_DIR = 'keys'

# SurveyTool settings
FLAVOR = DEV
DEBUG = True
TEMPLATE_DEBUG = True

CRONJOB_LOCK_PREFIX = 'lock.dev'

ALLOWED_EMAIL_ADDRESSES=['adamf@pobox.com', 'adamfeuer@gmail.com', 'robertreichner@gmail.com']

LOGIN_REDIRECT_URL = SITE_PREFIX + LOGIN_REDIRECT_BASE_URL
USERENA_SIGNIN_REDIRECT_URL = SITE_PREFIX + USERENA_SIGNIN_REDIRECT_BASE_URL
LOGIN_URL = SITE_PREFIX + LOGIN_BASE_URL
LOGOUT_URL = SITE_PREFIX + LOGOUT_BASE_URL
SIGNUP_SUCCESSFUL_URL = SITE_PREFIX + SIGNUP_SUCCESSFUL_BASE_URL
