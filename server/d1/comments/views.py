#coding:utf-8
from django.http import *
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
from time import gmtime, strftime
from django.shortcuts import render, render_to_response
from django.views.generic import *
from urlparse import urlparse

from comments.models import *
from d1.database import *

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

class CommentView(TemplateView):
    id_count = 0
    template_name = ""
    comment = ""

    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment', 'Empty Comment')
        leave_comment(comment, kwargs.get('refer_url'))
        return comment

    def get(self, request, *args, **kwargs):
        return comment_board(request, kwargs.get('text'))

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
        msgboards[refer_url] = []
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
    return leave_comment(refer_url, netloc)

@csrf_exempt 
def comment_board(request, refer_url_b64 = None):
    '''
    主要程序入口，读取URL中的BASE64字符串并打印到board上，并解析POST/GET的参数，
    进行相应的动作。
    '''
    #不管是否是post，都先解析字符串，把refer_url打到comment里
    if refer_url_b64:
        refer_url = base64.b64decode(refer_url_b64)
        netloc = urlparse(refer_url).netloc
        debug_comment(refer_url, netloc)
    #如果是POST，那么写comment_board
    if request.method == 'POST':
        write_comment_board(request, netloc)
    #然后返回新的HTML，刷新掉老的。这里用jquery动态加载回复。
    res = HttpResponse(get_comment_board_template(request, netloc))
    res['Access-Control-Allow-Origin'] = '*'
    return res

msgboards = {}    #区分URL的msgboards
messageBoard = [] #只有一个的全局messageBoard
cursor = 0