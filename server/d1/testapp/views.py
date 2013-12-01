from django.http import HttpResponse

import datetime

from django.views.generic import *
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from news.models import Article
from django.utils import timezone
from django.http import *

from testapp.models import *

class MyView(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

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

class ArticleCounterRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, pk):
        article = get_object_or_404(Article, pk=pk)
        article.update_counter()
        return reverse('product_detail', args=(pk,))

class CommentCreateView(CreateView):
    model = Comment
    template_name = 'testapp/comment_create_view.html'
    
    def get_success_url(self):
        return reverse('comment_list')

    def get_context_data(self, **kwargs):
        kwargs["object_list"] = Comment.objects.all()
        return super(CommentCreateView, self).get_context_data(**kwargs)

class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'testapp/comment_update_view.html'

class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        """
        Redirect to the page listing all of the proxy urls
        """
        return reverse('comment_detail')

    def get(self, *args, **kwargs):
        """
        This has been overriden because by default
        DeleteView doesn't work with GET requests
        """
        return self.delete(*args, **kwargs)

#DetailView: design to display data
class CommentDetailView(DetailView):
    model = Comment
    template_name = 'testapp/comment_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(CommentDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


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

def length_not_enough(request):
    html = "<html><body>length not enough</body></html>"
    return html

class TestAppView(TemplateView):
    def get(self, request, *args, **kwargs):
        print request
        print args
        print kwargs

    def post(self):
        pass

msgboards = dict()

messageBoard = list()
cursor = 0
