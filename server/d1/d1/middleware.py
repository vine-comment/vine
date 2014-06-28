from django.utils import timezone
from django.utils.html import strip_spaces_between_tags as short


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
