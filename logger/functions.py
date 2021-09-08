from logger.models import Log
from django.contrib.auth.models import AnonymousUser


def log_event(request, event, description=None, user=None):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if user is None and not isinstance(request.user, AnonymousUser):
        user = request.user

    Log(ip=ip, user=user, event=event, description=description).save()
