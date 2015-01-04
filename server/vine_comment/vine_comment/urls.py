# coding=utf-8

from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from vine_comment.views import *
from vine_comment.views import *
from vine_comment.forms import *

from django.contrib.auth.decorators import login_required


from registration.forms import RegistrationFormTermsOfService
from registration.backends.views import RegistrationView
from registration.backends.views import RegistrationSimpleView


# NOT USE NOW.
urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.urls')),
    url(r'^matrix/?$', TemplateView.as_view(template_name='matrix/matrix.html'), name='matrix'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url('', include('social.apps.django_app.urls', namespace='social')),
)

# TEST python-social-auth
urlpatterns = patterns('',
    (r'^search/', include('haystack.urls')),
    (r'^avatar/', include('avatar.urls')),
    url(r'^$', 'social_auth_app.views.comments'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup-email/', 'social_auth_app.views.signup_email'),
    url(r'^email-sent/', 'social_auth_app.views.validation_sent'),
    url(r'^login/$', 'social_auth_app.views.comments'),
    url(r'^logout/$', 'social_auth_app.views.logout'),
    url(r'^done/$', 'social_auth_app.views.done', name='done'),
    url(r'^email/$', 'social_auth_app.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    # 这个 social.apps.django_app.urls 实际上包含了所有social auth的处理逻辑：

    # url(r'^login/(?P<backend>[^/]+)/$', 'auth', name='begin'),
    # url(r'^complete/(?P<backend>[^/]+)/$', 'complete', name='complete'),
    # url(r'^disconnect/(?P<backend>[^/]+)/$', 'disconnect', name='disconnect'),
    # url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$', 'disconnect', name='disconnect_individual'),
)

urlpatterns += patterns('',
    url(r'^home/(?P<flag>.*?)/?$', login_required(HomeView.as_view()), name='home'),
    url(r'^user/head-sculpture/?$', login_required(UserHeadSculptureView.as_view()), name='user_head_sculpture'),
    # TODO social auth registration
    url(r'^accounts/', include('registration.backends.urls')),
    url(r'^comment/delete/(?P<id>.*?)/?$', CommentDeleteView.as_view(), name='comment_delete'),
    url(r'^comment/modify/(?P<id>.*?)/?$', CommentModifyView.as_view(), name='comment_modify'),
    url(r'^comment/(?P<url_b64>.*?)/(?P<flag>.*?)/?$', CommentView.as_view(), name='comment'),
    url(r'^ajax/comment/(?P<url_b64>.*?)/?$', CommentRawView.as_view(), name='comment_ajax'),
    url(r'^ajax/up/comment/(?P<id>.*?)/?$', CommentUpView.as_view(), name='comment_up'),
    url(r'^ajax/down/comment/(?P<id>.*?)/?$', CommentDownView.as_view(), name='comment_down'),
    url(r'^ajax/reply/comment/(?P<id>.*?)/?$', CommentReplyView.as_view(), name='comment_reply'),
	url(r'^ajax/showmsg/comment/(?P<url_b64>.*?)/?$', CommentShowMsgView.as_view(), name='comment_showmsg'),
    url(r'^ajax/showmsg/new/comment/(?P<flag>.*?)/?$', CommentShowNewListView.as_view(), name='comment_plugin_new'),
    url(r'^ajax/showmsg/hot/comment/(?P<flag>.*?)/?$', CommentShowHotListView.as_view(), name='comment_plugin_hot'),
    url(r'^ajax/showmsg/relevant/comment/(?P<flag>.*?)/?$', CommentShowRelevantListView.as_view(), name='comment_plugin_relevant'),
	#url(r'^ajax/youlike/comment/(?P<url_b64>.*?)/(?P<flag>.*?)/?$', CommentsTagView.as_view(), name='comment_youlike'),
    url(r'^comment_raw/(?P<url_b64>.*?)/?$', CommentRawView.as_view(), name='comment_raw'),
    # TODO like reddit..
    url(r'^detail/comment/(?P<id>[^/]+)/?$', CommentDetailView.as_view(), name="comment-detail"),
    url(r'^account/(?P<url_b64>.*?)/?$', AccountView.as_view(), name='account'),
    url(r'^account_raw/(?P<url_b64>.*?)/?$', AccountRawView.as_view(), name='account_raw'),
    url(r'^letter/(?P<url_b64>.*?)/?$', LetterView.as_view(), name='letter'),
    url(r'^letter_raw/(?P<url_b64>.*?)/?$', LetterRawView.as_view(), name='letter_raw'),
    url(r'^setting/(?P<url_b64>.*?)/?$', SettingView.as_view(), name='setting'),
    url(r'^setting_raw/(?P<url_b64>.*?)/?$', SettingRawView.as_view(), name='setting_raw'),
    url(r'^auth_test/$', TemplateView.as_view(template_name='social_signin.html'), name='auth_test'),
    url(r'^comments/hot/(?P<days>.*?)/?$', CommentsHotView.as_view(), name='comments_hot'),
    url(r'^comments/up/(?P<days>.*?)/?$', CommentsUpView.as_view(), name='comments_up'),
    url(r'^comments/debate/(?P<days>.*?)/?$', CommentsDebateView.as_view(), name='comments_debate'),
    url(r'^comments/best/?$', CommentsBestView.as_view(), name='comments_best'),
    url(r'^comments/tag/(?P<flag>.*?)/?$', CommentsTagView.as_view(), name='comments_tag'),
    url(r'^comments/related/(?P<url_b64>.*?)/?$', CommentsRelatedView.as_view(), name='comments_related'),
    url(r'^comments/newest/?$', CommentsNewestView.as_view(), name='comments_newest'),
    url(r'^comments/$', CommentsView.as_view(), name='comments'),
    url(r'^comments/urlpost/$', UrlpostView.as_view(), name='url_post'),
    url(r'^accounts/register/$',
          RegistrationView.as_view(form_class=VineRegistrationForm),
          name='registration_register'),
    url(r'^accounts/register/simple/$',
          RegistrationSimpleView.as_view(form_class=VineRegistrationForm),
          name='registration_register_simple'),
    url(r'^index$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

from haystack.views import SearchView, search_view_factory, FacetedSearchView
from haystack.forms import HighlightedModelSearchForm, FacetedSearchForm
from haystack.query import SearchQuerySet

# patterns 第一个参数是 prefix（对view的），所以这里是 haystack.views.SearchView (?)
urlpatterns += patterns('haystack.views',
    url(r'^advanced_search/', search_view_factory(
        view_class=SearchView,
        template='search/advanced_search.html',
        # 当前不需要sqs，它是用来filter某个范围的
        # searchqueryset=sqs,
        form_class=HighlightedModelSearchForm
    ), name='advanced_search'),
)

# 对title进行切片（facet）
# 以如下形式在模版里调用：
# {% for title in facets.fields.title|slice:":5" %}
sqs = SearchQuerySet().facet('title')

# patterns 第一个参数是 prefix（对view的），所以这里是 haystack.views.SearchView (?)
urlpatterns += patterns('haystack.views',
    url(r'^faceted_search/', search_view_factory(
        view_class=FacetedSearchView,
        template='search/faceted_search.html',
        searchqueryset=sqs,
        form_class=FacetedSearchForm
    ), name='faceted_search'),
)


urlpatterns += patterns('',
                    url(r'^captcha/', include('captcha.urls')),
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
    
