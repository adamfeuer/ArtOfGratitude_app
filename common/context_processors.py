from django.conf import settings
def settings_urls(request):
    return { 'base_url': settings.BASE_URL,
             'login_url': settings.LOGIN_URL,
             'media_url': settings.MEDIA_URL,
}


