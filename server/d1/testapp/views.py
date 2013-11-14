from django.http import HttpResponse
from django.views.generic import View, TemplateView, RedirectView

class MyView(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
    
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from news.models import Article

class ArticleCounterRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, pk):
        article = get_object_or_404(Article, pk=pk)
        article.update_counter()
        return reverse('product_detail', args=(pk,))