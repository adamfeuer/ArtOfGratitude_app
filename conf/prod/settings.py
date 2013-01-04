import ConfigParser
from gratitude.settings import *

APP_CONFIG = '/opt/gratitude/gratitude.config'
config = ConfigParser.RawConfigParser()
config.read(APP_CONFIG)
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

SITE_URL = "http://artofgratitude.com"
SITE_PREFIX = "/app"
BASE_URL = SITE_URL + SITE_PREFIX
SITE_ID = 1

STATIC_ROOT = '/opt/gratitude/gratitude/static'
STATIC_URL = '/app/static/'
LOGFILE_PATH = '/opt/gratitude/logs/gratitude.log'

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
                'filename': '/var/log/apache2/gratitude-django-request.log',
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
ENCRYPTED_FIELD_KEYS_DIR = '/opt/gratitude/gratitude/keys'

# SurveyTool settings
FLAVOR = PROD
DEBUG = False
TEMPLATE_DEBUG = False

CRONJOB_LOCK_PREFIX = 'lock.prod'

#FLAVOR = DEV
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_PHONE_NUMBERS = []
#ALLOWED_PHONE_NUMBERS = ['206-330-4774']

SIGNUP_SUCCESSFUL_URL = SITE_URL + SIGNUP_SUCCESSFUL_BASE_URL
