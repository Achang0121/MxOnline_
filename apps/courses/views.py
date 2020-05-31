from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Courses, CourseTag, CourseResource, Video
from apps.operations.models import UserFavorite, UserCourses, CourseComments


class CourseVideoView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, course_id, video_id, *args, **kwargs):
        course = Courses.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        
        video = Video.objects.get(id=int(video_id))
        
        # 用户和课程之间的关联
        user_course = UserCourses.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        
        course_resources = CourseResource.objects.filter(course=course)
        
        # 该课程的用户
        user_courses = UserCourses.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourses.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        # 该课程用户的其他课程
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        
        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses': related_courses,
            'video': video,
        })


class CourseCommentsView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        
        comments = CourseComments.objects.filter(course=course)
        
        user_course = UserCourses.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        course_resources = CourseResource.objects.filter(course=course)
        
        # 该课程的用户
        user_courses = UserCourses.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourses.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        # 该课程用户的其他课程
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses': related_courses,
            'comments': comments,
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        
        # 用户和课程之间的关联
        user_course = UserCourses.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        
        course_resources = CourseResource.objects.filter(course=course)
        
        # 该课程的用户
        user_courses = UserCourses.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourses.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        # 该课程用户的其他课程
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses': related_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        
        # 获取收藏状态
        is_fav_course = False
        is_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                is_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=3):
                is_fav_org = True
        # 课程推荐
        tag_list = course.coursetag_set.all()
        tags = [tag for tag in tag_list]
        course_tags = CourseTag.objects.filter(tag__in=tags).exclude(course__id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)
        
        return render(request, 'course-detail.html', {
            "course": course,
            "is_fav_course": is_fav_course,
            "is_fav_org": is_fav_org,
            "related_courses": related_courses,
        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """获取课程列表信息"""
        all_courses = Courses.objects.order_by('-add_time')
        hot_courses = Courses.objects.order_by('-click_nums')[:3]
        
        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        search_type = "course"
        if keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))
        
        # 对课程进行排序
        sort = request.GET.get('sort', '')
        if sort == "students":
            all_courses = all_courses.order_by('-students')
        elif sort == "hot":
            all_courses = all_courses.order_by('-click_nums')
        
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        
        p = Paginator(all_courses, per_page=9, request=request)
        courses = p.page(page)
        
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'search_type': search_type,
            'keywords': keywords,
            'sort': sort,
        })
