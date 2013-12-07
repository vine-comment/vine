from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from vine_comment.models import Comment

class LatestEntriesFeed(Feed):
    title = "New Comment"
    link = "/sitenews/"
    description = "Updates on changes and additions on Comments."

    def items(self):
        return Comment.objects.order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    # item_link is only needed if Comment has no get_absolute_url method.
    def item_link(self, item):
        return reverse('Comment', args=[item.pk])