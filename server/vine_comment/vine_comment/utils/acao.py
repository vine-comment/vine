#Access-Control-Allow-Origin

from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.utils.importlib import import_module

class ACAO(object):
    def process_response(self, request, response):
        if request.path.startswith('/static/'):
            response['Access-Control-Allow-Origin'] = '*'
        return response