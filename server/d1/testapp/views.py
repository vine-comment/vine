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




