#coding:utf-8
from django.http import *
from django.shortcuts import render
from django.views.generic import *
from django.core.paginator import Paginator
from django.utils.timezone import utc
#from django.core.context_processors import csrf

from urlparse import urlparse
import datetime
import base64

from models import Comment, CommentBoard

class CommentView(TemplateView):
    template_name = ""
    base64_default_str = 'aHR0cDovL3d3dy5udWxsLmNvbS8='
    index_default_str = 'http://www.null.com/'

    def _post_comment(self, index_url, comment_str):
        comment_board, created = CommentBoard.objects.get_or_create(url=index_url, title=urlparse(index_url).netloc)
        comment_board.save() if created else None
        comment = Comment(time_added = datetime.datetime.utcnow().replace(tzinfo=utc),
                          comment_str = comment_str,
                          comment_board = comment_board)
        comment.save()
        return

    def record_index_url(self, request, *args, **kwargs):
        index_url = kwargs.get('index_url', self.index_default_str)
        comment_str = index_url
        self._post_comment(index_url, comment_str)

    def debug(self, request, *args, **kwargs):
        self.record_index_url(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        comment_str = request.POST.get('comment', 'Empty Comment')
        index_url = kwargs.get('index_url', self.index_default_str)
        self._post_comment(index_url, comment_str)

    #TODO: https://github.com/frankban/django-endless-pagination
    def get(self, request, *args, **kwargs):
        index_page = request.GET.get('page', 1)
        index_url = kwargs.get('index_url', self.index_default_str)

        comments = Comment.objects.filter(comment_board__url__contains=index_url).order_by('-time_added')
        p = Paginator(comments, 5).page(index_page)
        return render(request, "comments/comment_view_raw.html", {
            'p_comment': p,
            'refer_url': index_url,
        })

    def dispatch(self, request, *args, **kwargs):
        url_b64 = kwargs.get('url_b64', self.base64_default_str)
        kwargs['index_url'] = base64.b64decode(url_b64)
        
        self.debug(request, *args, **kwargs)
        return super(CommentView, self).dispatch(request, *args, **kwargs)
