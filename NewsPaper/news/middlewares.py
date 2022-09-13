import pytz

from django.utils import timezone, translation

from .models import Author


class TimezoneMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.user_locale = None

    def __call__(self, request):
        self.user_locale = Author.objects.filter(author_user=request.user.id).exists()
        if self.user_locale:
            user_info = Author.objects.get(author_user=request.user.id)
            timezone.activate(user_info.timezone)
            request.session['django_timezone'] = user_info.timezone
            translation.activate(user_info.language)
        else:
            tzname = request.session.get('django_timezone')
            if tzname:
                timezone.activate(pytz.timezone(tzname))
            else:
                timezone.deactivate()
        return self.get_response(request)
