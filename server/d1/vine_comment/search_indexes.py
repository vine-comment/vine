import datetime
from haystack import indexes
from vine_comment.models import Comment


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    comment_str = indexes.CharField(model_attr='comment_str')
    title = indexes.CharField()
    author_ip = indexes.CharField(null=True)

    def get_model(self):
        return Comment

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(time_modified__lte=datetime.datetime.now())