import redis
from django import forms

from captcha.fields import CaptchaField

from apps.users.models import UserProfile
from MxOnline.settings import REDIS_HOST, REDIS_PORT


class UpdateMobileForm(forms.Form):
    code = forms.CharField(required=True, min_length=4, max_length=4)
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    
    def clean_code(self):
        mobile = self.data.get('mobile')
        code = self.data.get('code')
        redis_cli = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset='utf-8', decode_responses=True)
        redis_code = redis_cli.get(str(mobile))
        if redis_code != code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

    def clean(self):
        pwd1 = self.cleaned_data['password1']
        pwd2 = self.cleaned_data['password2']
        
        if pwd2 != pwd1:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', ]


class RegisterGetForm(forms.Form):
    captcha = CaptchaField(required=True)


class RegisterPostForm(forms.Form):
    code = forms.CharField(required=True, min_length=4, max_length=4)
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    password = forms.CharField(required=True, min_length=6, max_length=20)
    
    def clean_mobile(self):
        mobile = self.data.get('mobile')
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError('该手机号已经注册！')
        return mobile
    
    def clean_code(self):
        mobile = self.data.get('mobile')
        code = self.data.get('code')
        redis_cli = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset='utf-8', decode_responses=True)
        redis_code = redis_cli.get(str(mobile))
        if redis_code != code:
            raise forms.ValidationError("验证码不正确")
        return code


class DynamicLoginForm(forms.Form):
    captcha = CaptchaField()
    mobile = forms.CharField(required=True, min_length=11, max_length=11)


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=3, max_length=20)
    password = forms.CharField(required=True, min_length=6, max_length=20)


class DynamicLoginPostForm(forms.Form):
    code = forms.CharField(required=True, min_length=4, max_length=4)
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    
    def clean_code(self):
        mobile = self.data.get('mobile')
        code = self.data.get('code')
        redis_cli = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset='utf-8', decode_responses=True)
        redis_code = redis_cli.get(str(mobile))
        if redis_code != code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data
