from django.contrib.sites.models import Site
from django.conf import settings as django_settings

def settings(request):
    return { 'base_url': django_settings.BASE_URL,
             'login_url': django_settings.LOGIN_URL,
             'media_url': django_settings.MEDIA_URL,
             'site_prefix': django_settings.SITE_PREFIX,
           }

def site(request):
   return { 'site': Site.objects.get_current(),
          }
