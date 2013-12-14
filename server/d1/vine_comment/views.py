#coding:utf-8
from django.http import *
from django.shortcuts import render
from django.views.generic import *
from django.core.paginator import Paginator
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt

from urlparse import urlparse
import datetime
import base64

from models import Comment, CommentBoard

########################################################################
# 核心代码释义
#
# Client代码(tamper monkey)：
#   $('body').append('<div id="vine_comment_iframe"></div>');
#   $('#vine_comment_iframe').load("http://www.anwcl.com:8000/iframe/"
#     + btoa(document.location));
# 意即在body末尾append一个iframe，然后动态调用server流程
# 注：在extension中机制不同，extension中静态存储资源较多。
#
# Server整体流程：
# 1. 用户某插件(tamper monkey/chrome extension/etc.)访问CommentIframeView
#    ，返回到Client的html中
# 2. 浏览器自动根据iframe的信息访问CommentView，获得详细信息。
########################################################################

class CommentIframeView(TemplateView):
    template_name = 'comments/comment_iframe_view.html'
    index_default_str = 'http://www.null.com/'

    # 此view是server第一入口，回应iframe信息
    def get(self, request, *args, **kwargs):
        url_b64 = kwargs.get('url_b64', self.index_default_str)
        return render(request, self.template_name, {
            'url_b64': url_b64,
        })

class CommentView(TemplateView):
    template_name = ''
    base64_default_str = '' #aHR0cDovL3d3dy5udWxsLmNvbS8=
    index_default_str = '' #http://www.null.com/

    template_inside_cb = 'comments/comment_view_inside_comment_board.html'
    template_raw = 'comments/comment_view_raw.html'
    template_meta = 'comments/comment_view_meta.html'

    @csrf_exempt
    def _post_comment(self, index_url, comment_str):
        title=urlparse(index_url).netloc
        print title if title else 'Empty Title'
        comment_board, created = CommentBoard.objects.get_or_create(
                                    url=index_url,
                                    title=urlparse(index_url).netloc)
        comment_board.save() if created else None
        comment = Comment(
                    time_added = datetime.datetime.utcnow().replace(
                                    tzinfo=utc),
                    comment_str = comment_str,
                    comment_board = comment_board)
        comment.save()

    @csrf_exempt
    def record_index_url(self, request, *args, **kwargs):
        index_url = kwargs.get('index_url', self.index_default_str)
        comment_str = index_url
        self._post_comment(index_url, comment_str)

    @csrf_exempt
    def debug(self, request, *args, **kwargs):
        self.record_index_url(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        comment_str = request.POST.get('comment', 'Empty Comment')
        index_url = kwargs.get('index_url', self.index_default_str)
        self._post_comment(index_url, comment_str)
        
        kwargs['template'] = self.template_raw
        return self.get(request, *args, **kwargs)

    # 注：get方法除了正常request中调用，也会在post之后被调用，但template由post给出
    # TODO: https://github.com/frankban/django-endless-pagination
    def get(self, request, *args, **kwargs):
        #print request
        index_page = request.GET.get('page', 1)
        index_url = kwargs.get('index_url', self.index_default_str)

        comments = Comment.objects.filter(
                        comment_board__title__contains=\
                        urlparse(index_url).netloc).order_by('-time_added')
        p = Paginator(comments, 10).page(index_page)
        template_name = kwargs.get('template', self.template_meta)
        
        # BUG记录：2013/12/14，只有p_comment/refer_url作为入参时，无法返回页面（猜测是TEMPLATE渲染失败），但DEBUG返回200
        # 在主程中打印也没问题，但在template访问数据就不行。重启后问题消失。
        return render(request, template_name, {
            'p_comment': p,
            'refer_url': index_url,
        })

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        url_b64 = kwargs.get('url_b64', self.base64_default_str)
        kwargs['index_url'] = base64.b64decode(url_b64)
        
        #self.debug(request, *args, **kwargs)
        return super(CommentView, self).dispatch(request, *args, **kwargs)

class UserView(TemplateView):
    pass

class AccountView(TemplateView):
    pass

class LetterView(TemplateView):
    pass

class SettingView(TemplateView):
    pass

