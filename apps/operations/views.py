from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse

from apps.courses.models import Courses, Teachers
from apps.organizations.models import CourseOrg
from apps.operations.forms import UserFavoriteForm, CommentForm
from apps.operations.models import UserFavorite, CourseComments, Banner


class IndexView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all().order_by("index")
        courses = Courses.objects.filter(is_banner=False)[:6]
        banner_courses = Courses.objects.filter(is_banner=True)
        orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "banners": banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "orgs": orgs,
        })


class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        # 如果用户未登录，不能收藏
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录",
            })
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]
            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.comments = comments
            course_comment.course = course
            course_comment.save()
            return JsonResponse({
                "status": "success",
                "msg": "已收藏"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


class AddFavView(View):
    """用户点击收藏或取消收藏"""
    
    def post(self, request, *args, **kwargs):
        # 如果用户未登录，不能收藏
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录",
            })
        
        user_fav_form = UserFavoriteForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]
            
            # 是否已经收藏
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()
                
                if fav_type == 1:
                    course = Courses.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 3:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 2:
                    teacher = Teachers.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                
                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                
                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })
