from django.conf.urls import url

from .views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView, OrgTeachersView, OrgTeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='list'),
    url(r'^add_ask/$', AddAskView.as_view(), name='add_ask'),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),
    url(r'^(?P<org_id>\d+)/courses$', OrgCourseView.as_view(), name='courses'),
    url(r'^(?P<org_id>\d+)/desc$', OrgDescView.as_view(), name='desc'),
    url(r'^(?P<org_id>\d+)/teacher$', OrgTeacherView.as_view(), name='teacher'),
    url(r'^teachers/$', OrgTeachersView.as_view(), name='teachers'),
    url(r'^teachers/(?P<teacher_id>\d+)/$', OrgTeacherDetailView.as_view(), name='teacher_detail'),
]

