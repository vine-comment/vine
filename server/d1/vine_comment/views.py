#coding:utf-8
from django.http import *
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
from time import gmtime, strftime
from django.shortcuts import render, render_to_response
from django.views.generic import *
from urlparse import urlparse
from django.core.paginator import Paginator
import datetime
from django.utils.timezone import utc
import base64

from models import Comment, CommentBoard

class CommentView(TemplateView):
    template_name = ""
    base64_default_str = 'aHR0cDovL3d3dy5udWxsLmNvbS8='
    index_default_str = 'http://www.null.com/'

    def write_global_comment(self, request, *args, **kwargs):
        index_url = kwargs.get('index_url', self.index_default_str)
        comment_str = index_url
        comment_board, created = CommentBoard.objects.get_or_create(url = '', title = '')
        comment_board.save() if created else None
        comment = Comment(time_added = datetime.datetime.utcnow().replace(tzinfo=utc),
                          comment_str = comment_str,
                          comment_board = comment_board)
        comment.save()
        return

    def debug(self, request, *args, **kwargs):
        self.write_global_comment(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        comment_str = request.POST.get('comment', 'Empty Comment')
        index_url = kwargs.get('index_url', self.index_default_str)

        comment_board, created = CommentBoard.objects.get_or_create(url = index_url, title = urlparse(index_url).netloc)
        comment_board.save() if created else None
        comment = Comment(time_added = datetime.datetime.utcnow().replace(tzinfo=utc),
                          comment_str = comment_str,
                          comment_board = comment_board)
        comment.save()

        return 

    #TODO: https://github.com/frankban/django-endless-pagination
    def get(self, request, *args, **kwargs):
        index_page = request.GET.get('page', 1)
        index_url = kwargs.get('index_url', self.index_default_str)

        comments = Comment.objects.filter(comment_board__url__contains=index_url).order_by('-time_added')
        p = Paginator(comments, 5)

        template_name = "comments/comment_board_get.html"
        return render(request, template_name, {
            'messages': p.page(index_page).object_list,
            'blanks':  [0,] if p.num_pages > 1 else range(5 - p.count),
            'refer_url': index_url,
            'n_page': p.num_pages,
        })

    def dispatch(self, request, *args, **kwargs):
        url_b64 = kwargs.get('url_b64', self.base64_default_str)
        kwargs['index_url'] = base64.b64decode(url_b64)
        
        self.debug(request, *args, **kwargs)
        return super(CommentView, self).dispatch(request, *args, **kwargs)

    def __unicode__(self):
        return self.comment
