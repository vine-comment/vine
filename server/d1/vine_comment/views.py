#coding:utf-8

# python modules
from urlparse import urlparse
from datetime import timedelta
from random import sample
import datetime
import base64
import logging
import math
import sys
from bson import json_util
import json

# django modules
from django.http import *
from django.shortcuts import render, redirect
from django.views.generic import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from django_akismet_comments import AkismetModerator
from akismet import *

# 3rd party modules
import jieba
import jieba.analyse

# private modules
from vine_comment.models import Comment, CommentBoard, Reply, Author, Tag
from vine_comment.forms import *
from captcha.models import CaptchaStore

logger = logging.getLogger( __name__ )

########################################################################
# helpers
########################################################################
def login_stat(sender, user, request, **kwargs):
    authors = Author.objects.filter(user=user)
    if len(authors) > 0:
        author = authors[0]
    else:
        return

@receiver(user_logged_out)
def logout_stat(sender, user, request, **kwargs):
    update_last_request(request)
    authors = Author.objects.filter(user=user)
    if len(authors) > 0:
        author = authors[0]
    else:
        return
    author.last_request = datetime.datetime.utcnow().replace(tzinfo=utc)
    author.save()

#user_logged_in.connect(login_stat)
#user_logged_out.connect(logout_stat)

def update_last_request(request):
    # get now time just at a request arrived
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    if not request.user or not request.user.is_authenticated():
        return
    authors = Author.objects.filter(user=request.user)
    if len(authors) > 0:
        author = authors[0]
    else:
        return

    last_request = author.last_request

    days = now.day - last_request.day
    if days == 1:
        author.continuous_login += 1
        if author.continuous_login > author.history_c_login:
            author.history_c_login = author.continuous_login
    elif days > 1:
        author.continuous_login = 0 
    author.last_request = now
    author.save()
        


########################################################################
# 核心代码释义
#
# Client代码(tamper monkey)：
#   $('body').append('<div id="vine_comment_iframe"></div>');
#   $('#vine_comment_iframe').load("http://www.tengmanpinglun.com:8000/iframe/"
#     + btoa(document.location));
# 意即在body末尾append一个iframe，然后动态调用server流程
# 注：在extension中机制不同，extension中静态存储资源较多。
#
# Server整体流程：
# 1. 用户某插件(tamper monkey/chrome extension/etc.)访问CommentIframeView
#    ，返回到Client的html中
# 2. 浏览器自动根据iframe的信息访问CommentView，获得详细信息。
########################################################################

class CommentIframeView(TemplateView):
    template_name = 'comments/comment_iframe_view.html'
    index_default_str = 'http://www.null.com/'

    # 此view是server第一入口，回应iframe信息
    def get(self, request, *args, **kwargs):
        update_last_request(request)
        url_b64 = kwargs.get('url_b64', self.index_default_str)
        print "................."
        print request.path
        print "................."
        return render(request, self.template_name, {
            'url_b64': url_b64,
        })

class CommentView(TemplateView):
    template_name = ''
    base64_default_str = '' #aHR0cDovL3d3dy5udWxsLmNvbS8=
    index_default_str = '' #http://www.null.com/

    template_inside_cb = 'comments/comment_view_inside_comment_board.html'
    template_raw = 'comments/comment_view_raw.html'
    template_meta = 'comments/comment_view_meta.html'
    template_list = 'comments/comment_list.html'

    @csrf_exempt
    def _check_spam(self, index_url, comment_str, author_ip, user):
        #ak = Akismet(key=settings.AKISMET_API_KEY,blog_url='http://www.abfeucd')
        ak = Akismet(key='d56b9a5394bf',blog_url='http://www.abfeucd')

		try:
			if ak.verify_key():
				data = {
				'user_ip': '',
				'user_agent': '',
				'referrer': '',
				'comment_type': 'comment',
				'comment_author': '',
				}
				if ak.comment_check(comment=comment_str.encode('utf-8'), data=data, build_data=False):
				   #this is a spam
				   return True
				else :
				   return False
			else:
				return False
		except Exception as e:
			print e

		# Offline exception FIXME
		return False

    @staticmethod
    @csrf_exempt
    def _post_comment(index_url, comment_str, author_ip, user):
        title = urlparse(index_url).netloc

        # print comment_str, user
        logger.info(u'评论:' + comment_str
                     + u'IP:' + author_ip
                     + u' 用户:' + str(user)
                     + u' TITLE:' + title
                     + u' INDEX:' + index_url
                     + u' UTC:' + str(datetime.datetime.utcnow().replace(tzinfo=utc))
                     + u' Time:' + str(datetime.datetime.now()))

        comment_board, created = CommentBoard.objects.get_or_create(
                                    url=index_url,
                                    title=title)
        comment_board.save() if created else None
        if user and user.is_authenticated():
            author = get_author(user)
            comment = Comment(
                    time_added=datetime.datetime.utcnow().replace(
                                    tzinfo=utc),
                    time_modified=datetime.datetime.utcnow().replace(
                                    tzinfo=utc),
                    comment_str=comment_str,
                    comment_board=comment_board,
                    author_ip=author_ip,
                    title=title,
                    author=author)
            author.comments_sum += 1
            author.points += 5
            author.save()
        else:
            '''
            Annoymous User access the site.
            '''
            comment = Comment(
                    time_added=datetime.datetime.utcnow().replace(
                                    tzinfo=utc),
                    time_modified=datetime.datetime.utcnow().replace(
                                    tzinfo=utc),
                    comment_str=comment_str,
                    comment_board=comment_board,
                    title=title,
                    author_ip=author_ip)

        comment.save()#need to save here to create the ID
        # Generate top 5 tags for comment.
        stags= jieba.analyse.extract_tags(comment_str, topK=3)
        for stag in stags:
            tags = Tag.objects.filter(name=stag)
            if len(tags) > 0:
                comment.tags.append(tags[0])
                tags[0].comments.append(comment.id)
                tags[0].save()
            else:
                tag = Tag.objects.create(
                        name=stag,
                        time_added=datetime.datetime.utcnow().replace(
                                        tzinfo=utc),
                        )
                tag.comments.append(comment.id)
                tag.save()
                comment.tags.append(tag)
        #logger.info('tags: ' + repr(comment.tags).decode("unicode-escape"))
        comment.save()

    @csrf_exempt
    def record_index_url(self, request, *args, **kwargs):
        index_url = kwargs.get('index_url', self.index_default_str)
        author_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        user = request.user
        comment_str = index_url
        self._post_comment(index_url, comment_str, author_ip, user)

    @csrf_exempt
    def debug(self, request, *args, **kwargs):
        self.record_index_url(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        update_last_request(request)
        comment_str = request.POST.get('comment', 'Empty Comment')
        author_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        # For Nginx
        if not author_ip:
            author_ip = request.META.get('HTTP_X_FORWARDED_FOR', '0.0.0.0')
        index_url = kwargs.get('index_url', self.index_default_str)
        user = request.user
        logger.info(request.META)

        author = None
        if user.is_authenticated():
            author = get_author(user)
            is_not_human = author.is_not_human
        else:
            # CAPTCHA-FIXME: forbid annoymous user to comment.
            is_not_human = False

        if self._check_spam(index_url, comment_str, author_ip, user):
             logger.info(comment_str + ' this is a spam')
             if author is not None:
                 author.is_not_human = True
                 author.save()
        else:
             logger.info(comment_str + ' this is no a spam')
             if author is not None:
                 author.is_not_human = False
                 author.save()

        """
        if(is_not_human):
            captcha_key = request.POST.get('captcha_key', '')
            captcha_input_value= request.POST.get('captcha_value', '')

            form = CaptchaTestForm(request.POST)
            captcha_really_value = CaptchaStore.objects.get(hashkey=captcha_key)
            # Validate the form: the captcha field will automatically
            # check the input
            if (captcha_input_value == captcha_really_value.challenge):
                #is human
                self._post_comment(index_url, comment_str, author_ip, user)
                author.is_not_human = False
                author.save()
            else:
                #TODO return error to user
                print 'captcha error'
        else:
            """
        self._post_comment(index_url, comment_str, author_ip, user)

        #TODO in order to Refresh the captcha , it must be change commentBoard.js urls.py and template
        kwargs['template'] = self.template_list
        return self.get(request, *args, **kwargs)

    # 注：get方法除了正常request中调用，也会在post之后被调用，但template由post给出
    # TODO: https://github.com/frankban/django-endless-pagination
    def get(self, request, *args, **kwargs):
        update_last_request(request)
        #print request
        index_page = request.GET.get('page', 1)
        index_url = kwargs.get('index_url', self.index_default_str)
        url_b64 = kwargs.get('url_b64', self.base64_default_str)
        flag = kwargs['flag']

        #HOT
        comments_hot = Comment.objects.order_by('-time_added').filter(time_added__gte=datetime.datetime.now()-timedelta(days=30))
        comments_hot = sorted(comments_hot,key=lambda o:len(o.up_users),reverse=True)
        #comments_hot = filter(lambda x:urlparse(index_url).netloc in x.comment_board.title,
        #        Comment.objects.order_by('-time_added'))
        p_hot = Paginator(comments_hot, 3).page(1)

		#NEW
        comments_new = Comment.objects.order_by('-time_added').all()
        p_new = Paginator(comments_new, 3).page(1)

		#RELEVANT
        index_url = base64.b64decode(url_b64)
        url_objects = Url.objects.filter(url=index_url)
        if len(url_objects) == 0:
            print "No tag"
            # return HttpResponse('No tag: '+index_url, mimetype='plain/text')
            p_tag = p_hot
        else :
            tags = filter(lambda x:url_objects[0].id in x.urls, Tags.objects.order_by('-time_added'))
            if len(tags) == 0:
                print "No tag"
                p_tag = p_hot
            else :
                tags = sorted(tags,key=lambda x:len(x.comments),reverse=True)[0:10]
                count = len(tags)
                if count > 3:
                    tags = sample(tags, 3)
                else:
                    tags = sample(tags, count)

                for tag in tags:
                    comments = filter(lambda x: x.id in tag.comments, Comment.objects.all())
                    print "comments:", comments
                    tag.comments_list = sorted(comments,key=lambda x:len(x.up_users)-len(x.down_users),reverse=True)[0:3]

                index_page = request.GET.get('page', 1)
                print "index_page:", index_page

                logger.info(str(len(tags)) + ': ' + str(tags))
                p_tag = Paginator(tags, 3).page(1)

        template_name = kwargs.get('template', self.template_meta)
        form = CaptchaTestForm()

        user = request.user
        if user.is_authenticated():
            author = get_author(user)
            is_not_human = author.is_not_human
        else:
            # CAPTCHA-FIXME: forbid annoymous user to comment.
            is_not_human = False

        if flag == 'raw':
            template_name = 'comments/comment_list_raw.html'

        return render(request, template_name, {
			'p_comment_hot': p_hot,
            'p_comment_new': p_new,
            'p_comment_tag': p_tag,
            'index_url': index_url,
            'url_b64': url_b64,
            'form': form,
            'is_not_human': is_not_human,
        })

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        url_b64 = kwargs.get('url_b64', self.base64_default_str)
        kwargs['index_url'] = base64.b64decode(url_b64)

        #self.debug(request, *args, **kwargs)
        return super(CommentView, self).dispatch(request, *args, **kwargs)

class CommentDeleteView(TemplateView):

    def get(self, request, id):
        update_last_request(request)
        comments = Comment.objects.filter(id=id)
        if len(comments) == 0:
            return HttpResponse(status=404)
        comment = comments[0]
        for tag in comment.tags:
            tag.comments.remove(comment.id)
            tag.save()
        comment.delete()
        return HttpResponseRedirect('/comments/')

class CommentModifyView(TemplateView):

    def post(self, request, id):
        update_last_request(request)
        comment_str = request.POST.get('comment_str',None)
        comment_tags = request.POST.get('comment_tags',None)
        comments = Comment.objects.filter(id=id)
        if len(comments) == 0 or (not comment_str and not comment_tags):
            return HttpResponse(status=404)
        comment = comments[0]
        if comment_str:
            comment.comment_str = comment_str

        for tag in comment.tags:
            tag.comments.remove(comment.id)
            tag.save()
        comment.tags = []
        if comment_tags:
            stags = comment_tags.split(',')
            #TODO: duplicated stag case
            for stag in stags:
                tags = Tag.objects.filter(name=stag)
                if len(tags) > 0:
                    comment.tags.append(tags[0])
                    tags[0].comments.append(comment.id)
                    tags[0].save()
                else:
                    tag = Tag.objects.create(
                            name=stag,
                            time_added=datetime.datetime.utcnow().replace(
                                        tzinfo=utc),
                            )
                    tag.comments.append(comment.id)
                    tag.save()
                    comment.tags.append(tag)
        comment.save()
        return HttpResponse(status=200)

		# This view is used for ajax load, see commentBoard.js for more details.
class CommentShowMsgView(TemplateView):
    template_name = ''
    base64_default_str = '' #aHR0cDovL3d3dy5udWxsLmNvbS8=
    index_default_str = '' #http://www.null.com/

    template_list = 'comments/comment_list.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        #print request
        index_page = request.GET.get('page', 1)
        index_url = kwargs.get('index_url', self.index_default_str)
        url_b64 = kwargs.get('url_b64', self.base64_default_str)

        #HOT
        comments_hot = Comment.objects.order_by('-time_added').filter(time_added__gte=datetime.datetime.now()-timedelta(days=30))
        comments_hot = sorted(comments_hot,key=lambda o:len(o.up_users),reverse=True)
        #comments_hot = filter(lambda x:urlparse(index_url).netloc in x.comment_board.title,
        #        Comment.objects.order_by('-time_added'))
        p_hot = Paginator(comments_hot, 3).page(1)

		#NEW
        comments_new = Comment.objects.order_by('-time_added').all()
        p_new = Paginator(comments_new, 3).page(1)


		#RELEVANT
        index_url = base64.b64decode(url_b64)
        url_objects = Url.objects.filter(url=index_url)
        if len(url_objects) == 0:
            print "No tag"
            # return HttpResponse('No tag: '+index_url, mimetype='plain/text')
            p_tag = p_hot
        else :
            tags = filter(lambda x:url_objects[0].id in x.urls, Tags.objects.order_by('-time_added'))
            if len(tags) == 0:
                print "No tag"
                p_tag = p_hot
            else :
                tags = sorted(tags,key=lambda x:len(x.comments),reverse=True)[0:10]
                count = len(tags)
                if count > 3:
                    tags = sample(tags, 3)
                else:
                    tags = sample(tags, count)

                for tag in tags:
                    comments = filter(lambda x: x.id in tag.comments, Comment.objects.all())
                    print "comments:", comments
                    tag.comments_list = sorted(comments,key=lambda x:len(x.up_users)-len(x.down_users),reverse=True)[0:3]

                index_page = request.GET.get('page', 1)
                print "index_page:", index_page

                logger.info(str(len(tags)) + ': ' + str(tags))
                p_tag = Paginator(tags, 3).page(1)

        template_name = kwargs.get('template', self.template_list)

        return render(request, template_name, {
            'p_comment_tag': p_tag,
            'p_comment_hot': p_hot,
            'p_comment_new': p_new,
            'index_url': index_url,
            'url_b64': url_b64,
        })

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        url_b64 = kwargs.get('url_b64', self.base64_default_str)
        kwargs['index_url'] = base64.b64decode(url_b64)

        #self.debug(request, *args, **kwargs)
        return super(CommentShowMsgView, self).dispatch(request, *args, **kwargs)

# This view is used for ajax load, see commentBoard.js for more details.
class CommentRawView(TemplateView):
    template_name = ''
    base64_default_str = '' #aHR0cDovL3d3dy5udWxsLmNvbS8=
    index_default_str = '' #http://www.null.com/

    template_inside_cb = 'comments/comment_view_inside_comment_board.html'
    template_raw = 'comments/comment_view_raw.html'
    template_meta = 'comments/comment_view_meta.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        #print request
        index_page = request.GET.get('page', 1)
        index_url = kwargs.get('index_url', self.index_default_str)
        url_b64 = kwargs.get('url_b64', self.base64_default_str)

        #TODO performance optimization for objects order_by('-time_added')
        comments = filter(lambda x:urlparse(index_url).netloc in x.comment_board.title,
                Comment.objects.order_by('-time_added'))
        p = Paginator(comments, 10).page(index_page)
        template_name = kwargs.get('template', self.template_raw)

        return render(request, template_name, {
            'p_comment': p,
            'index_url': index_url,
            'url_b64': url_b64,
        })

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        url_b64 = kwargs.get('url_b64', self.base64_default_str)
        kwargs['index_url'] = base64.b64decode(url_b64)

        #self.debug(request, *args, **kwargs)
        return super(CommentRawView, self).dispatch(request, *args, **kwargs)

class UserView(TemplateView):
    pass

class AccountView(TemplateView):
    template_name = 'comments/account_view.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        return render(request, self.template_name)

class LetterView(TemplateView):
    template_name = 'comments/letter_view.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        return render(request, self.template_name)

class SettingView(TemplateView):
    template_name = 'comments/setting_view.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        return render(request, self.template_name)

class AccountRawView(TemplateView):
    template_name = 'comments/account_raw.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        return render(request, self.template_name)

class LetterRawView(TemplateView):
    template_name = 'comments/letter_raw.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        return render(request, self.template_name)

class SettingRawView(TemplateView):
    template_name = 'comments/setting_raw.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        return render(request, self.template_name)

class CommentUpView(TemplateView):
    def get(self, request, id):
        update_last_request(request)
        if not request.user.is_authenticated():
            return HttpResponse('non-user', mimetype='plain/text')
        comments = Comment.objects.filter(id=id)
        if not comments:
            return HttpResponse(status=404)
        comment = comments[0]
        if request.user.id in comment.up_users:
            comment.up_users.remove(request.user.id)
            comment.save()
            return HttpResponse('up-1', mimetype='plain/text')
        if request.user.id in comment.down_users:
            comment.down_users.remove(request.user.id)
            comment.save()
            comment.up_users.append(request.user.id)
            comment.save()
            return HttpResponse('down-1,up+1', mimetype='plain/text')
        else:
            comment.up_users.append(request.user.id)
            comment.save()
            return HttpResponse("up+1", mimetype='plain/text')

class CommentDownView(TemplateView):
    def get(self, request, id):
        update_last_request(request)
        if not request.user.is_authenticated():
            return HttpResponse('non-user', mimetype='plain/text')
        comments = Comment.objects.filter(id=id)
        if not comments:
            return HttpResponse(status=404)
        comment = comments[0]
        if request.user.id in comment.down_users:
            comment.down_users.remove(request.user.id)
            comment.save()
            return HttpResponse('down-1', mimetype='plain/text')
        if request.user.id in comment.up_users:
            comment.up_users.remove(request.user.id)
            comment.save()
            comment.down_users.append(request.user.id)
            comment.save()
            return HttpResponse('up-1,down+1', mimetype='plain/text')
        else:
            comment.down_users.append(request.user.id)
            comment.save()
            return HttpResponse("down+1", mimetype='plain/text')


class CommentReplyView(TemplateView):
    template_name = 'reply.html'

    def get(self, request, id):
        update_last_request(request)
        comments = Comment.objects.filter(id=id)
        if not comments:
            return HttpResponse(status=404)
        comment = comments[0]
        #replies = filter(lambda x: x.id in comment.replies, Reply.objects.all())
        return render(request, self.template_name, {
            'replies': comment.replies,
        })

    def post(self, request, id):
        update_last_request(request)
        comments = Comment.objects.filter(id=id)
        reply_str = request.POST.get('reply_str')
        if not comments:
            return HttpResponse(status=404)
        comment = comments[0]
        if request.user.is_authenticated():
            reply_obj = Reply.objects.create(
                        comment=comment,
                        user=request.user,
                        author_ip=request.META.get('REMOTE_ADDR', '0.0.0.0'),
                        time_added=datetime.datetime.utcnow().replace(
                                        tzinfo=utc),
                        reply_str=reply_str)
        else:
            '''
            Annoymous User access the site.
            '''
            reply_obj = Reply.objects.create(
                        comment=comment,
                        author_ip=request.META.get('REMOTE_ADDR', '0.0.0.0'),
                        time_added=datetime.datetime.utcnow().replace(
                                        tzinfo=utc),
                        reply_str=reply_str)
        reply_obj.save()
        comment.replies.append(reply_obj)
        comment.save()
        return HttpResponseRedirect('/ajax/reply/comment/'+id)

def expected_rating(o):
    ups = len(o.up_users)
    downs = len(o.down_users)
    n = ups + downs;
    if n == 0:
        score = 0
    else:
        z = 1.96
        phat = ups / n
        score = (phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
    return score

class CommentsView(TemplateView):

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        return HttpResponseRedirect('/comments/best')

class CommentsTagView(TemplateView):
    template_name = 'comments_tag.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        flag = kwargs['flag']
        if flag == 'simple':
            self.template_name = 'comments_tag_simple.html'
        if flag == 'raw':
            self.template_name = 'comments_tag_raw.html'
        if flag == 'plug':
            self.template_name = 'comments/comments_you_like.html'
        tags = Tag.objects.order_by('-time_added').all()
        if len(tags) == 0:
            print "No tag"
            # return HttpResponse('No tag', mimetype='plain/text')
        tags = sorted(tags,key=lambda x:len(x.comments),reverse=True)[0:10]
        count = len(tags)
        if count > 3:
            tags = sample(tags, 3)
        else:
            tags = sample(tags, count)

        for tag in tags:
            comments = filter(lambda x: x.id in tag.comments, Comment.objects.all())
            print "comments:", comments
            tag.comments_list = sorted(comments,key=lambda x:len(x.up_users)-len(x.down_users),reverse=True)[0:3]

        index_page = request.GET.get('page', 1)
        print "index_page:", index_page


        #TODO performance optimization for objects order_by('-time_added')
        logger.info(str(len(tags)) + ': ' + str(tags))
        try:
            p = Paginator(tags, 5).page(index_page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p = Paginator(tags, 5).page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p = Paginator(tags, 5).page(paginator.num_pages)

        return render(request, self.template_name, {
            'p_comment': p,
            'flag': flag,
        })

class CommentsRelatedView(TemplateView):
    template_name = 'comments_list_tag.html'

    def get(self, request, url_b64):
        update_last_request(request)
        index_url = base64.b64decode(url_b64)
        url_objects = Url.objects.filter(url=index_url)
        if len(url_objects) == 0:
            print "No tag"
            # return HttpResponse('No tag: '+index_url, mimetype='plain/text')

        tags = filter(lambda x:url_objects[0].id in x.urls, Tags.objects.order_by('-time_added'))
        if len(tags) == 0:
            return HttpResponse('No related tag', mimetype='plain/text')
        tags = sorted(tags,key=lambda x:len(x.comments),reverse=True)[0:10]
        count = len(tags)
        if count > 3:
            tags = sample(tags, 3)
        else:
            tags = sample(tags, count)

        for tag in tags:
            comments = filter(lambda x: x.id in tag.comments, Comment.objects.all())
            print "comments:", comments
            tag.comments_list = sorted(comments,key=lambda x:len(x.up_users)-len(x.down_users),reverse=True)[0:3]

        index_page = request.GET.get('page', 1)
        print "index_page:", index_page


        #TODO performance optimization for objects order_by('-time_added')
        logger.info(str(len(tags)) + ': ' + str(tags))
        try:
            p = Paginator(tags, 5).page(index_page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p = Paginator(tags, 5).page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p = Paginator(tags, 5).page(paginator.num_pages)

        return render(request, self.template_name, {
            'p_comment': p,
        })

class CommentsBestView(TemplateView):
    template_name = 'comments_best.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        comments = Comment.objects.order_by('-time_added').all()
        comments = sorted(comments,key=lambda x:len(x.up_users)-len(x.down_users),reverse=True)
        comments = sorted(comments,key=lambda x:expected_rating(x),reverse=True)
        index_page = request.GET.get('page', 1)
        print "index_page:", index_page


        #TODO performance optimization for objects order_by('-time_added')
        logger.info(str(len(comments)) + ': ' + str(comments))
        try:
            p = Paginator(comments, 10).page(index_page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p = Paginator(comments, 10).page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p = Paginator(comments, 10).page(paginator.num_pages)

        return render(request, self.template_name, {
            'p_comment': p,
        })

class CommentsNewestView(TemplateView):
    template_name = 'comments_newest.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        comments = Comment.objects.order_by('-time_added').all()
        comments = sys.modules['__builtin__'].list(comments)
        index_page = request.GET.get('page', 1)
        print "index_page:", index_page


        #TODO performance optimization for objects order_by('-time_added')
        logger.info(str(len(comments)) + ': ' + str(comments))
        try:
            p = Paginator(comments, 10).page(index_page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p = Paginator(comments, 10).page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p = Paginator(comments, 10).page(paginator.num_pages)

        return render(request, self.template_name, {
            'p_comment': p,
        })

class CommentsHotView(TemplateView):
    template_name = 'comments_hot.html'

    def get(self, request, days):
        update_last_request(request)
# need to use time_modified instead of time added
        comments = Comment.objects.order_by('-time_added').filter(time_added__gte=datetime.datetime.now()-timedelta(days=eval(days)))
        comments = sorted(comments,key=lambda o:len(o.replies),reverse=True)
        index_page = request.GET.get('page', 1)
        print "index_page:", index_page


        #TODO performance optimization for objects order_by('-time_added')
        logger.info(str(len(comments)) + ': ' + str(comments))
        try:
            p = Paginator(comments, 10).page(index_page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p = Paginator(comments, 10).page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p = Paginator(comments, 10).page(paginator.num_pages)

        return render(request, self.template_name, {
            'p_comment': p,
            'days': days,
        })

class CommentsUpView(TemplateView):
    template_name = 'comments_up.html'

    def get(self, request, days):
        update_last_request(request)
# need to use time_modified instead of time added
        comments = Comment.objects.order_by('-time_added').filter(time_added__gte=datetime.datetime.now()-timedelta(days=eval(days)))
        comments = sorted(comments,key=lambda o:len(o.up_users),reverse=True)
        index_page = request.GET.get('page', 1)
        print "index_page:", index_page


        #TODO performance optimization for objects order_by('-time_added')
        logger.info(str(len(comments)) + ': ' + str(comments))
        try:
            p = Paginator(comments, 10).page(index_page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p = Paginator(comments, 10).page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p = Paginator(comments, 10).page(paginator.num_pages)

        return render(request, self.template_name, {
            'p_comment': p,
            'days': days,
        })

def debate_index(o):
    ups = len(o.up_users)
    downs = len(o.down_users)
    summ = ups+downs
    diff = abs(ups-downs)
    if summ == 0:
        return float('inf')
    return diff/summ

class CommentsDebateView(TemplateView):
    template_name = 'comments_debate.html'

    def get(self, request, days):
        update_last_request(request)
# need to use time_modified instead of time added
        comments = Comment.objects.order_by('-time_added').filter(time_added__gte=datetime.datetime.now()-timedelta(days=eval(days)))
        comments = sorted(comments,key=lambda o:debate_index(o))
        index_page = request.GET.get('page', 1)
        print "index_page:", index_page


        #TODO performance optimization for objects order_by('-time_added')
        logger.info(str(len(comments)) + ': ' + str(comments))
        try:
            p = Paginator(comments, 10).page(index_page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p = Paginator(comments, 10).page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p = Paginator(comments, 10).page(paginator.num_pages)

        return render(request, self.template_name, {
            'p_comment': p,
            'days': days,
        })


class CommentShowNewListView(TemplateView):
    template_name = 'comments/comments_plugin_new.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
# need to use time_modified instead of time added
        flag = kwargs['flag']

		#NEW
        comments_new = Comment.objects.order_by('-time_added').all()
        if flag == 'max':
            p = Paginator(comments_new, 10).page(1)
        else :
            p = Paginator(comments_new, 3).page(1)


        return render(request, self.template_name, {
            'p_comment_new': p,
        })

class CommentShowHotListView(TemplateView):
    template_name = 'comments/comments_plugin_hot.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
# need to use time_modified instead of time added
        flag = kwargs['flag']

        comments_hot = Comment.objects.order_by('-time_added').filter(time_added__gte=datetime.datetime.now()-timedelta(days=30))
        comments_hot = sorted(comments_hot,key=lambda o:len(o.up_users),reverse=True)
        if flag == 'max':
            p = Paginator(comments_hot, 10).page(1)
        else :
            p = Paginator(comments_hot, 3).page(1)

        return render(request, self.template_name, {
            'p_comment_hot': p,
        })

class CommentDetailView(TemplateView):
    template_name = 'comments/comment_detail_view.html'

    def get(self, request, id, *args, **kwargs):
        update_last_request(request)
        comment = Comment.objects.filter(id=id)[0]
        return render(request, self.template_name, {'comment': comment})

def get_author(user):
    if not user.is_authenticated():
        return None
    authors = Author.objects.filter(user=user)
    if authors:
        author = authors[0]
    else:
        author = Author.objects.create(
            user=user,
            time_added=datetime.datetime.utcnow().replace(tzinfo=utc)
            )
        author.save()
    return author

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        flag = kwargs['flag']
        if flag == 'simple':
            self.template_name = 'home_simple.html'
        author = get_author(request.user)
        index_page = request.GET.get('page', 1)

        #TODO performance optimization for objects order_by('-time_added')
        comments = Comment.objects.filter(author=author)
        comments = comments.order_by('-time_added')
        comments = sys.modules['__builtin__'].list(comments)
        logger.info(str(len(comments)) + ': ' + str(comments))
        try:
            p = Paginator(comments, 10).page(index_page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p = Paginator(comments, 10).page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p = Paginator(comments, 10).page(paginator.num_pages)

        return render(request, self.template_name, {
            'header_form': UploadHeadSculptureForm,
            'p_comment': p,
            'flag': flag,
        })

class UserHeadSculptureView(TemplateView):

    def get(self, request, *args, **kwargs):
        update_last_request(request)
        return HttpResponseForbidden('allowed only via POST')

    def post(self, request, *args, **kwargs):
        update_last_request(request)
        form = UploadHeadSculptureForm(request.POST, request.FILES)
        if form.is_valid():
            author = get_author(request.user)
            if not author:
                return redirect(request.META.get('HTTP_REFERER', '/'))
            author.picture = form.cleaned_data['image']
            author.save()
            # XXX success hint
            return redirect(request.META.get('HTTP_REFERER', '/'))
        return redirect(request.META.get('HTTP_REFERER', '/'))

