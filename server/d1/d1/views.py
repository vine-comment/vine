#coding:gbk
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
    comment_tuple = [strftime("%Y-%m-%d %H:%M:%S", gmtime()), len(messageBoard), comment]
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
    #获得最后15条
    last_messages = reversed(messageBoard[-15:])
    #如果多余15条，翻页
    page_count = len(messageBoard) / 15 + 1
    
    html = "<html><body>"
    for message in last_messages:
        for ele in message:
            html += str(ele) + ' '
        html += '<br>'
    for i in range(1, page_count + 1):
        html += str(i) + ' '
    html += '<br>'
    html += "</body></html>"
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