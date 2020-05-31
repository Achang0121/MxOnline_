from django.conf.urls import url

from apps.users.views import UserInfoView, UserImageUploadView, UserUpdatePasswordView, UserUpdateMobileView, \
    MyCoursesView, MyFavOrgView, MyFavCourseView, MyFavTeacherView, MyMessagesView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/$', UserImageUploadView.as_view(), name='image_upload'),
    url(r'^update/pwd/$', UserUpdatePasswordView.as_view(), name='update_pwd'),
    url(r'^update/mobile/$', UserUpdateMobileView.as_view(), name='update_mobile'),
    url(r'^my_courses/$', MyCoursesView.as_view(), name='my_courses'),
    url(r'^my_fav_org/$', MyFavOrgView.as_view(), name='my_fav_org'),
    url(r'^my_fav_course/$', MyFavCourseView.as_view(), name='my_fav_course'),
    url(r'^my_fav_teacher/$', MyFavTeacherView.as_view(), name='my_fav_teacher'),
    url(r'^messages/$', MyMessagesView.as_view(), name='my_messages'),
]
