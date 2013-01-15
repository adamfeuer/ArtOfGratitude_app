import os, sys

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

MEDIA_URL = '/media/'
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
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "common.context_processors.settings_urls",
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
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
    'gratitude.profiles',
    'gratitude.gratitude',
    'gratitude.gratitude.cron',

)

# Django email settings
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = '/tmp/gratitude-email.log' 
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
DEFAULT_FROM_EMAIL = '"Art of Gratitude" <team@artofgratitude.com>'

# Userena settings
USERENA_ACTIVATION_REQUIRED = True 
AUTH_PROFILE_MODULE = 'profiles.Profile'
USERENA_WITHOUT_USERNAMES = True
USERENA_DISABLE_PROFILE_LIST = True
USERENA_MUGSHOT_SIZE = 140

# Userena base urls
LOGIN_REDIRECT_BASE_URL = '/profile/%(username)s/'
LOGIN_BASE_URL = '/accounts/signin/'
LOGOUT_BASE_URL = '/accounts/signout/'
SIGNUP_SUCCESSFUL_BASE_URL = "/signup-verification"

# Userena activation email
USERENA_SEND_EMAIL_MODULE='gratitude.gratitude.EmailSender'
USERENA_ACTIVATION_EMAIL_MESSAGE_TEMPLATE='gratitude/emails/activation_email_message.html'
USERENA_SIGNUP_FIRST_AND_LAST_NAMES=True
 
# Test settings
TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

# Guardian
ANONYMOUS_USER_ID = -1

# Gratitude App
VERSION = "0.1"
PROD = "prod"
TEST = "test"
DEV = "dev"


