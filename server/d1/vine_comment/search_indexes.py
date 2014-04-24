# python
import datetime

# django
from django.contrib.auth.models import User

# third-party
from haystack import indexes

# vine
from vine_comment.models import Comment


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    comment_str = indexes.CharField(model_attr='comment_str')
    # if we set facet to True, then the title would stored as
    # *title* and *title_exact*.
    title = indexes.CharField(faceted=True)
    author_ip = indexes.CharField(null=True)
    # Another example:
    # pub_date = DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Comment

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(time_modified__lte=datetime.datetime.now())

'''
# All User Fields
class AllUserIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = User
'''
'''
# All Fields
class AllCommentIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Comment

# Blacklisted Fields
class LimitedCommentIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Comment
        excludes = ['user']

# Whitelisted Fields
class CommentIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Comment
        fields = ['user', 'pub_date']

    # Note that regular ``SearchIndex`` methods apply.
    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return Comment.objects.filter(pub_date__lte=datetime.datetime.now())
'''
