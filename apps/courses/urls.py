from django.conf.urls import url

from apps.courses.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentsView, CourseVideoView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="list"),
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
    url(r'^(?P<course_id>\d+)/lessons/$', CourseLessonView.as_view(), name="lessons"),
    url(r'^(?P<course_id>\d+)/comments/$', CourseCommentsView.as_view(), name="comments"),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)$', CourseVideoView.as_view(), name="video"),
]
