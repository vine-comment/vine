#coding:utf-8
from django.http import *
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
from time import gmtime, strftime

from d1.database import *
from django.shortcuts import render, render_to_response

from django.views.generic import *
from urlparse import urlparse
from comments.models import *

@csrf_exempt 
def write(request, words):
    if request.method == 'POST':
        write_comment_board(request)
    messageBoard.append(words)
    html = "<html><body>"
    for i, message in enumerate(messageBoard):
        output = str(i) + ': ' + message + '<br>'
        html += output
    
    html += "</body></html>"
    return HttpResponse(html)

#每个URL单独一个CommentBoard
class CommentBoardView(TemplateView):
    count = 0
    def __init__(self, url):
        pass
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        c = Comment(title="test-title", content="test-content")
        c.save()
        pass
    def delete(self, request, *args, **kwargs):
        pass
    def put(self, request, *args, **kwargs):
        pass
    def get_context_data(self, **kwargs):
        context = super(CommentBoardView, self).get_context_data(**kwargs)
        context['latest_articles'] = Comment.objects.all()[:5]
        return context

#ListView: Represent a list of objects
class CommentListView(ListView):
    model = Comment
    context_object_name = 'latest_comment_list'
    template_name = 'comments/comment_list_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(CommentListView, self).get_context_data(**kwargs)
#         return context

class CommentView(TemplateView):
    id_count = 0
    template_name = ""
    comment = ""
    
    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment', 'None Comment - Invalid')
        self.id_count += 1
        comment_tuple = [datetime.date.today(), cursor, comment]
        self.msgboard.append(comment_tuple)
        return comment

    def get(self, request, *args, **kwargs):
        html = "<html><body>"
        for message in self.msgboard:
            for ele in message:
                html += str(ele) + ' '
            html += '<br>'
        html += "</body></html>"
        return html

    @csrf_exempt 
    def __call__(self, request):
        if request.method == 'POST':
            self.write(request)
        elif request.method == 'GET':
            pass
        res = HttpResponse(self.get(request))
        res['Access-Control-Allow-Origin'] = '*'
        return res

    def __unicode__(self):
        return self.comment

import base64
def leave_comment(comment, refer_url):
    #len(messageBoard), 
    
    comment_tuple = [strftime("%Y-%m-%d %H:%M:%S", gmtime()), comment]
    messageBoard.append(comment_tuple)
    
    if not msgboards.has_key(refer_url):
        msgboards[refer_url] = list()
    msgboards[refer_url].append(comment_tuple)
    
def write_comment_board(request, refer_url):
    comment = request.POST.get('comment', 'Empty Comment')
    leave_comment(comment, refer_url)

    return comment

def get_comment_board_template(request, refer_url):
    req_page = request.GET.get('page', None)
    if req_page is None or req_page is '':
        req_page = 1

    COMMENT_PER_PAGE = 5
    end_comment = (-req_page)*COMMENT_PER_PAGE
    start_comment = (1-req_page)*COMMENT_PER_PAGE
    if start_comment is 0:
        start_comment = None
    
    if refer_url is None:
        msgboard = messageBoard
    else:
        msgboard = msgboards.get(refer_url)
        if msgboard is None:
            #FIXME invalid case
            pass
    
    #获得最后COMMENT_PER_PAGE条
    to_show_messages = reversed(msgboard[end_comment:start_comment])
    #如果多余COMMENT_PER_PAGE条，翻页
    page_count = len(msgboard) / COMMENT_PER_PAGE + 1
    
    #render html here
    template_name = "comments/comment_board_get.html"
    return render(request, template_name, {
        'messages': to_show_messages,
        'n_messages': len(msgboard),
        'message_per_page': COMMENT_PER_PAGE,
        'refer_url': refer_url,
        'n_page': page_count + 1,
    })

def debug_comment(refer_url, netloc):
    leave_comment(refer_url, netloc)

@csrf_exempt 
def comment_board(request, refer_url_b64 = None):
    if refer_url_b64:
        refer_url = base64.b64decode(refer_url_b64)
        netloc = urlparse(refer_url).netloc
        debug_comment(refer_url, netloc)
    if request.method == 'POST':
        write_comment_board(request, netloc)
    elif request.method == 'GET':
        pass
    res = HttpResponse(get_comment_board_template(request, netloc))
    res['Access-Control-Allow-Origin'] = '*'
    return res

msgboards = dict()
messageBoard = list()
cursor = 0