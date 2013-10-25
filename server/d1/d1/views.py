#coding:utf-8
from django.http import *
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
from time import gmtime, strftime
import datetime
from d1.database import *
#from django.shortcuts import render

from urlparse import urlparse

def hello(request):
    return HttpResponse("Hello world")

def hi(request):
    return HttpResponse("Hi!")

def time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

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

class Comment(object):
    id_count = 0
    msgboard = list()
    
    def write(self, request):
        if request.POST.has_key('comment'):
            comment = request.POST['comment']
        else:
            comment = 'None Comment - Invalid'
        self.id_count += 1
        comment_tuple = [datetime.date.today(), cursor, comment]
        self.msgboard.append(comment_tuple)
        return comment

    def get(self, request):
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
    
    def __init__(self):
        pass


import base64
def leave_comment(comment, refer_url):
    #len(messageBoard), 
    
    comment_tuple = [strftime("%Y-%m-%d %H:%M:%S", gmtime()), comment]
    messageBoard.append(comment_tuple)
    
    if not msgboards.has_key(refer_url):
        msgboards[refer_url] = list()
    msgboards[refer_url].append(comment_tuple)
    
def write_comment_board(request, refer_url):
    
    if request.POST.has_key('comment'):
        comment = request.POST['comment']
    else:
        comment = 'Empty Comment'
    leave_comment(comment, refer_url)
    
    return comment

def length_not_enough(request):
    html = "<html><body>length not enough</body></html>"
    return html

def get_comment_board(request, refer_url):
    #if specified page
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
    
    html = '<ul class="list-group">'
    #html = "<html><body>"
    for message in to_show_messages:
        #TODO 账户控制
        html += '<li class="list-group-item">'
        html += '<strong>路人甲</strong> '
        for ele in message:
            html += ele.encode('utf8') + ' '
        html += '<br>'#<hr/>
        html += '</li>'
    
    #如果不足 COMMENT_PER_PAGE ，则补齐
    if len(msgboard) < COMMENT_PER_PAGE:
        for i in range(COMMENT_PER_PAGE - len(msgboard)):
            html += '<li class="list-group-item">'
            html += '<br><br>'
            html += '</li>'
        
    html += '</ul>'
    
    html += '<div><ul class="pagination">'
    html += '<li><a href="#">«</a></li>'
    for i in range(1, page_count + 1):
        #onclick page load
        html += '<li><a href="#">'
        html += str(i)
        html += '</a></li>'
    html += '<li><a href="#">»</a></li>'
    html += '</ul></div>'

    #html += "</body></html>"
    return html

@csrf_exempt 
def comment_board(request, refer_url_b64 = None):
    if refer_url_b64:
        refer_url = base64.b64decode(refer_url_b64)
        netloc = urlparse(refer_url).netloc
        leave_comment(netloc, netloc)
    if request.method == 'POST':
        write_comment_board(request, netloc)
    elif request.method == 'GET':
        pass
    res = HttpResponse(get_comment_board(request, netloc))
    res['Access-Control-Allow-Origin'] = '*'
    return res

def test_func(request, comment_in_url):
    if comment_in_url:
        leave_comment(comment_in_url)
    if request.method == 'POST':
        write_comment_board(request)
    elif request.method == 'GET':
        pass
    res = HttpResponse(get_comment_board(request))
    res['Access-Control-Allow-Origin'] = '*'
    return res

def home(request):
    html = ''
    return HttpResponse(html)

#init
msgboards = dict()

messageBoard = list()
cursor = 0