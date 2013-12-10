from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from d1.views import *
from vine_comment.views import *

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'comment/(?P<url_b64>.*?)/?$', CommentView.as_view(), name='comment'),
    url(r'iframe/(?P<url_b64>.*?)/?$', CommentIframeView.as_view(), name='comment_iframe'),
)

from functools import wraps
from django.contrib.staticfiles.views import serve as serve_static

if settings.DEBUG:

    def custom_headers(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            response['Access-Control-Allow-Origin'] = '*'
            return response

        return wrapper

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', custom_headers(serve_static)),
    )
    