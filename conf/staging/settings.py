from gratitude.settings import *

module = sys.modules[__name__]
appConfigFile = '/opt/gratitude-staging/gratitude.config'
createModuleGlobalsFromConfigFile(module, appConfigFile)

SITE='staging.artofgratitude.com'
SITE_URL = 'https://' + SITE
SITE_PREFIX = '/app'
BASE_URL = SITE_URL 
SITE_ID = 1
FORCE_SCRIPT_NAME = SITE_PREFIX

STATIC_ROOT = '/opt/gratitude-staging/gratitude/static'
STATIC_URL = '/app/static/'
LOGFILE_PATH = '/opt/gratitude-staging/logs/gratitude.log'

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
ENCRYPTED_FIELD_KEYS_DIR = '/opt/gratitude-staging/gratitude/keys'

# Application settings
FLAVOR = PROD
DEBUG = False
TEMPLATE_DEBUG = False
CRONJOB_LOCK_PREFIX = 'lock.prod'

#FLAVOR = DEV
#DEBUG = True
#TEMPLATE_DEBUG = True

ALLOWED_EMAIL_ADDRESSES=[]

# full urls
LOGIN_REDIRECT_URL = SITE_PREFIX + LOGIN_REDIRECT_BASE_URL
USERENA_SIGNIN_REDIRECT_URL = SITE_PREFIX + USERENA_SIGNIN_REDIRECT_BASE_URL
LOGIN_URL = SITE_PREFIX + LOGIN_BASE_URL
LOGOUT_URL = SITE_PREFIX + LOGOUT_BASE_URL
LOGIN_ERROR_URL = SITE_PREFIX + LOGIN_ERROR_BASE_URL
SIGNUP_SUCCESSFUL_URL = SITE_PREFIX + SIGNUP_SUCCESSFUL_BASE_URL
USERENA_SIGNIN_REDIRECT_URL = SITE_PREFIX + USERENA_SIGNIN_REDIRECT_BASE_URL
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = SITE_PREFIX + SOCIAL_AUTH_NEW_USER_REDIRECT_BASE_URL
SOCIAL_AUTH_BACKEND_ERROR_URL = SITE_PREFIX + SOCIAL_AUTH_BACKEND_ERROR_BASE_URL

# Gratitude settings
DJANGO_PROCESS_NAME = 'manage.py runserver'
APACHE_PROCESS_NAME = 'apache2'
