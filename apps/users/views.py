from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger
import redis

from apps.courses.models import Courses
from apps.operations.models import UserCourses, UserFavorite, UserMessage, Banner
from apps.organizations.models import CourseOrg, Teachers
from apps.users.models import UserProfile
from apps.utils.yunpian import send_single_sms
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm, \
    UploadImageForm, UserInfoForm, ChangePasswordForm, UpdateMobileForm
from apps.utils.random_str import generate_random
from MxOnline.settings import YUNPIAN_API_KEY, REDIS_HOST, REDIS_PORT


class CustomAuth(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class MyMessagesView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        
        for message in messages:
            message.is_read = True
            message.save()
        
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        
        p = Paginator(messages, per_page=9, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        teachers = []
        
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teachers.objects.get(id=fav_teacher.fav_id)
            teachers.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        courses = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course = Courses.objects.get(id=fav_course.fav_id)
            courses.append(course)
        
        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyCoursesView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        my_courses = UserCourses.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'my_courses': my_courses,
        })


class UserUpdateMobileView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def post(self, request, *args, **kwargs):
        mobile_form = UpdateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data['mobile']
            # 已经存在的记录不能重复使用
            if request.user.mobile == mobile:
                return JsonResponse({
                    'mobile': '与当前手机号一致',
                })
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    'mobile': '该手机号已经被占用',
                })
            else:
                user = request.user
                user.mobile = mobile
                user.username = mobile
                user.save()
                # logout(request) # 可选择是否推出
                return JsonResponse({
                    'status': 'success',
                })
        else:
            return JsonResponse(mobile_form.errors)


class UserUpdatePasswordView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def post(self, request, *args, **kwargs):
        pwd_form = ChangePasswordForm(request.POST)
        if pwd_form.is_valid():
            # 验证表单，也可以在form中去验证
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return JsonResponse({
                    'status': 'fail',
                    'msg': '密码不一致',
                })
            user = request.user
            user.set_password(pwd1)
            user.save()
            # 修改密码成功后，会要求重新登陆，如果不想退出，就再登陆下即可
            login(request, user)
            
            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse(pwd_form.errors)


class UserImageUploadView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse({
                'status': 'fail',
            })


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        captcha_form = RegisterGetForm()
        
        return render(request, 'usercenter-info.html', {
            'captcha_form': captcha_form,
        })
    
    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse(user_info_form.errors)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        banners = Banner.objects.all()[:3]
        return render(request, 'register.html', {
            'register_get_form': register_get_form,
            'banners': banners,
        })
    
    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        banners = Banner.objects.all()[:3]
        if register_post_form.is_valid():
            # 验证表单成功
            mobile = register_post_form.cleaned_data['mobile']
            password = register_post_form.cleaned_data['password']
            # 新建用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            register_get_form = RegisterGetForm()
            return render(request, 'register.html', {
                'register_get_form': register_get_form,
                'register_post_form': register_post_form,
                'banners': banners,
            })


class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        banners = Banner.objects.all()[:3]
        
        next = request.GET.get('next', '')
        login_form = DynamicLoginForm()
        return render(request, 'login.html', {
            'login_form': login_form,
            'next': next,
            'banners': banners,
        })
    
    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        banners = Banner.objects.all()[:3]
        dynamic_login = True
        if login_form.is_valid():
            # 没有注册账号，依然可以登录
            mobile = login_form.cleaned_data['mobile']
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                # 新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)  # 随机生成10位的数字+字母+特殊字符的密码
                user.set_password(password)  # 给密码加密
                user.mobile = mobile
                user.save()
            login(request, user)
            next = request.GET.get('next', '')
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse('index'))
        else:
            d_form = DynamicLoginForm()
            return render(request, 'login.html', {
                'login_form': login_form,
                'dynamic_login': dynamic_login,
                'd_form': d_form,
                'banners': banners,
            })


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data['mobile']
            # 随机生成数字验证码
            code = generate_random(4, 0)
            # re_json = send_single_sms(YUNPIAN_API_KEY, code=code, mobile=mobile)
            # if re_json['code'] == 0:
            #     re_dict['status'] = 'success'
            redis_cli = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset='utf-8', decode_responses=True)
            redis_cli.set(str(mobile), code)
            redis_cli.expire(str(mobile), 60 * 5)  # 设置短信验证码5分钟过期
            # else:
            #     re_dict['msg'] = re_json['msg']
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        next = request.GET.get('next', '')
        login_form = DynamicLoginForm()
        banners = Banner.objects.all()[:3]
        
        return render(request, 'login.html', {
            'login_form': login_form,
            'next': next,
            'banners': banners,
        })
    
    def post(self, request, *args, **kwargs):
        # 表单验证
        login_form = LoginForm(request.POST)
        banners = Banner.objects.all()[:3]
        
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            
            # 验证用户是否存在
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                next = request.GET.get('next', '')
                # 登录成功后跳转到首页
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('index'))
            else:
                # 未查询到用户
                
                return render(request, 'login.html', {
                    'message': '用户名或密码错误',
                    'login_form': login_form,
                    'banners': banners,
                })
        else:
            return render(request, 'login.html', {
                'login_form': login_form,
                'banners': banners,
            })
