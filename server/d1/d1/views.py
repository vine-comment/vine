#coding:utf-8
from django.http import *
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
from time import gmtime, strftime
import datetime
#from django.shortcuts import render

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
    messageBoard = {}
    
    def write(self, request):
        if request.POST.has_key('comment'):
            comment = request.POST['comment']
        else:
            comment = 'None Comment - Invalid'
        self.id_count += 1
        comment_tuple = [datetime.date.today(), cursor, comment]
        messageBoard.append(comment_tuple)
        return comment

    def get(self, request):
        html = "<html><body>"
        for message in messageBoard:
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


def leave_comment(comment):
    #len(messageBoard), 
    comment_tuple = [strftime("%Y-%m-%d %H:%M:%S", gmtime()), comment]
    messageBoard.append(comment_tuple)
    
def write_comment_board(request):
    
    if request.POST.has_key('comment'):
        comment = request.POST['comment']
    else:
        comment = 'None Comment - Invalid'
    leave_comment(comment)
    
    return comment

def length_not_enough(request):
    html = "<html><body>length not enough</body></html>"
    return html

def get_comment_board(request):
    #if specified page
    req_page = request.GET.get('page', None)
    if req_page is None or req_page is '':
        req_page = 1

    COMMENT_PER_PAGE = 5
    end_comment = (-req_page)*COMMENT_PER_PAGE
    start_comment = (1-req_page)*COMMENT_PER_PAGE
    if start_comment is 0:
        start_comment = None
    
    #获得最后COMMENT_PER_PAGE条
    to_show_messages = reversed(messageBoard[end_comment:start_comment])
    #如果多余COMMENT_PER_PAGE条，翻页
    page_count = len(messageBoard) / COMMENT_PER_PAGE + 1
    
    html = '<ul class="list-group">'
    #html = "<html><body>"
    for message in to_show_messages:
        html += '<li class="list-group-item">'
        html += '<strong>Anonymous</strong> <br>'
        for ele in message:
            html += str(ele) + ' '
        html += '<br>'#<hr/>
        html += '</li>'
    
    #如果不足 COMMENT_PER_PAGE ，则补齐
    if len(messageBoard) < COMMENT_PER_PAGE:
        for i in range(COMMENT_PER_PAGE - len(messageBoard)):
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
def comment_board(request, comment_in_url = None):
    if comment_in_url:
        leave_comment(comment_in_url)
    if request.method == 'POST':
        write_comment_board(request)
    elif request.method == 'GET':
        pass
    res = HttpResponse(get_comment_board(request))
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
messageBoard = list()
cursor = 0