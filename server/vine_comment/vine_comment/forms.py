#coding:utf-8
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import *

from captcha.fields import CaptchaField

class UrlpostForm(forms.Form):
    #TODO: url integrity checking
    url  = forms.CharField(widget=forms.Textarea)
    comment_str  = forms.CharField(widget=forms.Textarea, label="comment")

class CaptchaTestForm(forms.Form):
#    myfield = AnyOtherField()
    captcha = CaptchaField()

class VineRegistrationForm(forms.Form):
    required_css_class = 'required'

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label="用户名",
                                error_messages={'invalid': "只能包含数字、字母、与@/./+/-/_等符号。"})
    email = forms.EmailField(label="邮箱")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="密码")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="密码 (重复)")
    # is_human = forms.NullBooleanField(label="你是人类吗？", required=False)
    # dob = forms.DateField(label="生日 (例子: 1999-2-19)", required=False)
    # phone = forms.CharField(label="手机", required=False)
    # gender = forms.CharField(label="性别", required=False)

    def clean_username(self):
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("用户名已存在。")
        else:
            return self.cleaned_data['username']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("两次输入的密码不一致。")
        return self.cleaned_data
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("此email地址已被使用，请使用不同的email地址。"))
        return self.cleaned_data['email']


class UploadHeadSculptureForm(forms.Form):
    image = forms.ImageField(label='上传图片')

