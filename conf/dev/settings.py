from gratitude.settings import *

module = sys.modules[__name__]
appConfigFile = os.path.join(os.environ['WORKON_HOME'], 'gratitude', 'gratitude.config')
createModuleGlobalsFromConfigFile(module, appConfigFile)

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
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOGFILE_PATH,
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': 'logs/django_request.log',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
        'email_sender': {
                'level':'DEBUG',
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
#FLAVOR = PROD 
#DEBUG = False
#TEMPLATE_DEBUG = False
FLAVOR = DEV
#DEBUG = True
DEBUG = False
TEMPLATE_DEBUG = True

CRONJOB_LOCK_PREFIX = 'lock.dev'

ALLOWED_EMAIL_ADDRESSES=['adamf@pobox.com', 'adamfeuer@gmail.com', 'robertreichner@gmail.com', 'abbypatricia108108@gmail.com']

# full urls
LOGIN_REDIRECT_URL = SITE_PREFIX + LOGIN_REDIRECT_BASE_URL
USERENA_SIGNIN_REDIRECT_URL = SITE_PREFIX + USERENA_SIGNIN_REDIRECT_BASE_URL
LOGIN_URL = SITE_PREFIX + LOGIN_BASE_URL
LOGOUT_URL = SITE_PREFIX + LOGOUT_BASE_URL
SIGNUP_SUCCESSFUL_URL = SITE_PREFIX + SIGNUP_SUCCESSFUL_BASE_URL
USERENA_SIGNIN_REDIRECT_URL = SITE_PREFIX + USERENA_SIGNIN_REDIRECT_BASE_URL
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = SITE_PREFIX + SOCIAL_AUTH_NEW_USER_REDIRECT_BASE_URL
SOCIAL_AUTH_BACKEND_ERROR_URL = SITE_PREFIX + SOCIAL_AUTH_BACKEND_ERROR_BASE_URL

# Gratitude settings
DJANGO_PROCESS_NAME = 'manage.py runserver'
APACHE_PROCESS_NAME = 'httpd'
