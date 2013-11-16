#coding:utf-8
from django.http import *
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
from time import gmtime, strftime
import datetime
from d1.database import *
from d1.models import *
from django.shortcuts import render
from django.shortcuts import render_to_response

from django.views.generic import TemplateView, DetailView
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

from models import *
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

from django.utils import timezone

#DetailView: design to display data
class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comments/comment_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(CommentDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

#ListView: Represent a list of objects
class CommentListView(DetailView):
    model = Comment
    context_object_name = 'latest_comment_list'
    template_name = 'comments/comment_list_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(CommentListView, self).get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context

class CommentView(TemplateView):
    id_count = 0
    template_name = ""
    comment = ""

    def __init__(self, comment_str = None):
        
        #genr time
        
        #genr id
        
        #genr url
        
        pass
    
    def post(self, request):
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
    
    if request.POST.has_key('comment'):
        comment = request.POST['comment']
    else:
        comment = 'Empty Comment'
    leave_comment(comment, refer_url)
    
    return comment

def length_not_enough(request):
    html = "<html><body>length not enough</body></html>"
    return html

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
        leave_comment(refer_url, netloc)
    if request.method == 'POST':
        write_comment_board(request, netloc)
    elif request.method == 'GET':
        pass
    res = HttpResponse(get_comment_board_template(request, netloc))
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

from django.http import HttpResponse
from django.views.generic import ListView
from books.models import Book

class BookListView(ListView):
    model = Book

    def head(self, *args, **kwargs):
        last_book = self.get_queryset().latest('publication_date')
        response = HttpResponse('')
        # RFC 1123 date format
        response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

class AboutView(TemplateView):
    template_name = "about.html"

#init
msgboards = dict()

messageBoard = list()
cursor = 0