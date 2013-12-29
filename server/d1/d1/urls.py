from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from d1.views import *
from vine_comment.views import *

from app.views import home, done, logout, error, form, form2, close_login_popup
from app.facebook import facebook_view
from app.vkontakte import vkontakte_view
from app.odnoklassniki import ok_app, ok_app_info

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^matrix/?$', TemplateView.as_view(template_name='matrix/matrix.html'), name='matrix'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'', include('social_auth.urls')),
    url(r'^test/$', TemplateView.as_view(template_name='comments/test.html')),
)

urlpatterns += patterns('',
    url(r'^comment/(?P<url_b64>.*?)/?$', CommentView.as_view(), name='comment'),
    url(r'^account/(?P<url_b64>.*?)/?$', AccountView.as_view(), name='account'),
    url(r'^letter/(?P<url_b64>.*?)/?$', LetterView.as_view(), name='letter'),
    url(r'^setting/(?P<url_b64>.*?)/?$', SettingView.as_view(), name='setting'),
)

# django-social-auth
urlpatterns += patterns('',
    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^form2/$', form2, name='form2'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', facebook_view, name='fb_app'),
    url(r'^vk/', vkontakte_view, name='vk_app'),
    url(r'^ok/$', ok_app, name='ok_app'),
    url(r'^ok/info/$', ok_app_info, name='ok_app_info'),
    url(r'^close_login_popup/$', close_login_popup, name='login_popup_close'),
    url(r'', include('social_auth.urls')),
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
        url(r'iframe/(?P<url_b64>.*?)/?$', custom_headers(CommentIframeView.as_view()), name='comment_iframe'),
        url(r'^static/(?P<path>.*)$', custom_headers(serve_static)),
    )
    