from django.utils.html import strip_spaces_between_tags as short

class SpacelessMiddleware(object):
    def process_response(self, request, response):
        if 'text/html' in response.get('Content-Type', {}):
            response.content = short(response.content)
        return response
