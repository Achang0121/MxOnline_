"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

import xadmin

from apps.users.views import LoginView, LogoutView, SendSmsView, DynamicLoginView, RegisterView
from apps.operations.views import IndexView
from MxOnline.settings import MEDIA_ROOT  # STATIC_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('d_login/', DynamicLoginView.as_view(), name='d_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name='send_sms'),
    
    # 机构相关页面
    url(r'^org/', include(('apps.organizations.urls', 'organizations'), namespace='org')),
    
    # 课程相关页面
    url(r'^course/', include(('apps.courses.urls', 'courses'), namespace='course')),
    
    # 用户相关的操作页面
    url(r'^op/', include(('apps.operations.urls', 'operations'), namespace='op')),
    
    # 配置上传文件的访问URL
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    
    # 配置static文件的访问URL
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    
    # 用户个人中心
    url(r'^users/', include(('apps.users.urls', 'users'), namespace='users')),
    
    # 配置uEditor相关的URL
    url(r'ueditor/', include('DjangoUeditor.urls')),

]
