from django.contrib import admin
from vine_comment.models import Comment, CommentBoard

admin.site.register(Comment)
admin.site.register(CommentBoard)