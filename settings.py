import os, sys, ConfigParser
from django.contrib.messages import constants as messages

def createModuleGlobalsFromConfigFile(module, filepath):
   config = ConfigParser.RawConfigParser() 
   config.read(filepath) 
   setattr(module,'TWILIO_FROM_PHONE_NUMBER', config.get('Twilio', 'TWILIO_FROM_PHONE_NUMBER'))
   setattr(module,'TWILIO_ACCOUNT', config.get('Twilio', 'TWILIO_ACCOUNT'))
   setattr(module,'TWILIO_TOKEN', config.get('Twilio', 'TWILIO_TOKEN'))
   setattr(module,'DATABASE_HOST', config.get('Database', 'host'))
   setattr(module,'DATABASE_USER', config.get('Database', 'user'))
   setattr(module,'DATABASE_PASSWORD', config.get('Database', 'password')) 
   setattr(module,'DATABASE_DB', config.get('Database', 'database')) 
   setattr(module,'AWS_ACCESS_KEY_ID', config.get('AWS', 'user')) 
   setattr(module,'AWS_SECRET_ACCESS_KEY', config.get('AWS', 'password')) 
   setattr(module,'FACEBOOK_APP_ID', config.get('Facebook', 'app_id')) 
   setattr(module,'FACEBOOK_API_SECRET', config.get('Facebook', 'api_secret')) 

abspath = lambda *p: os.path.abspath(os.path.join(*p))

PROJECT_ROOT = abspath(os.path.dirname(__file__))
USERENA_MODULE_PATH = abspath(PROJECT_ROOT, '..')
sys.path.insert(0, USERENA_MODULE_PATH)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Adam Feuer', 'adamf@pobox.com'),
)

MANAGERS = ADMINS

#if DEBUG:
    # Use the Python SMTP debugging server. You can run it with:
    # ``python -m smtpd -n -c DebuggingServer localhost:1025``.
#    EMAIL_PORT = 1025

# We're using Apache mod_proxy and gunicorn - use this so redirects work
USE_X_FORWARDED_HOST = True 

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'

ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
)

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = abspath(PROJECT_ROOT, 'media')
DOCUMENT_ROOT = abspath(PROJECT_ROOT, 'docs')

MEDIA_URL = '/app/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
STATIC_URL = '/app/'

SECRET_KEY = 'sx405#tc)5m@s#^jh5l7$k#cl3ekg)jtbo2ds(n(kw@gp0t7x@'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'userena.middleware.UserenaLocaleMiddleware',
    'common.middleware.RuntimePathsMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "common.context_processors.settings",
    "common.context_processors.site",
    "social_auth.context_processors.social_auth_by_name_backends",
    "social_auth.context_processors.social_auth_backends",
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social_auth.backends.facebook.FacebookBackend',
)

ROOT_URLCONF = 'gratitude.urls'

TEMPLATE_DIRS = (
    abspath(PROJECT_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'gunicorn',
    'easy_thumbnails',
    'guardian',
    'south',
    'userena',
    'userena.contrib.umessages',
    'django_ses',
    'adminplus',
    'cronjobs',
    'crispy_forms',
    'tastypie',
    'social_auth',
    'gratitude.profiles',
    'gratitude.gratitude',
    'gratitude.gratitude.cron',

)

# Bootstrap CSS for django alerts
MESSAGE_TAGS = {
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info',
    messages.WARNING: 'alert',
    messages.ERROR: 'alert alert-error',
}

# Django email settings
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = '/tmp/gratitude-email.log' 
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
DEFAULT_FROM_EMAIL = '"Art of Gratitude" <team@artofgratitude.com>'

# Django Social Auth
SOCIAL_AUTH_DEFAULT_USERNAME = 'social_auth_user'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_NEW_USER_REDIRECT_BASE_URL = '/social-verification/'
SOCIAL_AUTH_BACKEND_ERROR_BASE_URL = '/signup-error/'
SOCIAL_AUTH_INACTIVE_USER_BASE_URL = '/login-error/'
SOCIAL_AUTH_INACTIVE_USER_MESSAGE = 'Your account is not yet verified. Please check your email and save your first gratitudes to activate your account and start your 30 days of gratitude!'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# Userena settings
USERENA_ACTIVATION_REQUIRED = True 
AUTH_PROFILE_MODULE = 'profiles.Profile'
USERENA_WITHOUT_USERNAMES = True
USERENA_DISABLE_PROFILE_LIST = True
USERENA_MUGSHOT_SIZE = 140
USERENA_REMEMBER_ME_DAYS = ('3 years', 1095)
USERENA_ACTIVATION_DAYS = 35

# Userena base urls
LOGIN_REDIRECT_BASE_URL = '/profile/'
LOGIN_BASE_URL = '/'
LOGOUT_BASE_URL = '/signout/'
SIGNUP_SUCCESSFUL_BASE_URL = "/signup-verification"

# Userena activation email
USERENA_SEND_EMAIL_MODULE='gratitude.gratitude.EmailSender'
USERENA_ACTIVATION_EMAIL_MESSAGE_TEMPLATE='gratitude/emails/activation_email_body.html'
USERENA_ACTIVATION_EMAIL_SUBJECT_TEMPLATE='gratitude/emails/activation_email_subject.txt'
USERENA_SIGNUP_FIRST_AND_LAST_NAMES=True
USERENA_SIGNIN_REDIRECT_BASE_URL = LOGIN_REDIRECT_BASE_URL
#USERENA_SIGNIN_REDIRECT_BASE_URL='/profile/%(username)s/'
 
# Test settings
TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

# Guardian
ANONYMOUS_USER_ID = -1

# Gratitude App 
VERSION = "0.2"
PROD = "prod"
TEST = "test"
DEV = "dev"
MAX_STASHED_GRATITUDES=270
MAX_AGE_OF_STASHED_GRATITUDES_IN_DAYS=90
GRATITUDES_PER_DAY = 3
DAYS_OF_GRATITUDE = 30
REMINDER_EMAIL_DAYS = [1, 3, 7, 30]

# Gratitude Analytics Actions
MAX_ACTIONS_PER_DAY = 1000

