import pytz
import pygeoip

from django.utils import timezone
from django.utils.html import strip_spaces_between_tags as short
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from .signals import detected_timezone
from .utils import get_ip_address_from_request


class SpacelessMiddleware(object):
    def process_response(self, request, response):
        if 'text/html' in response.get('Content-Type', {}):
            response.content = short(response.content)
        return response


class TimezoneMiddleware(object):
    def process_request(self, request):
        tz = request.session.get("django_timezone")
        print tz
        if tz:
            timezone.activate(tz)


GEOIP_DATABASE = getattr(settings, 'GEOIP_DATABASE', None)

if not GEOIP_DATABASE:
    raise ImproperlyConfigured("GEOIP_DATABASE setting has not been defined.")


db_loaded = False
db = None


def load_db():
    global db
    db = pygeoip.GeoIP(GEOIP_DATABASE, pygeoip.MEMORY_CACHE)

    global db_loaded
    db_loaded = True


class AutoTimezoneMiddleware(object):
    def process_request(self, request):
        if not db_loaded:
            load_db()

        tz = request.session.get('django_timezone')

        if not tz:
            # use the default timezone (settings.TIME_ZONE) for localhost
            tz = timezone.get_default_timezone()

            ip = get_ip_address_from_request(request)
            if ip != '127.0.0.1':
                # if not local, fetch the timezone from pygeoip
                tz = db.time_zone_by_addr(ip)

        if tz:
            timezone.activate(tz)
            detected_timezone.send(sender=get_user_model(), instance=request.user, timezone=tz)
        else:
            timezone.deactivate()
