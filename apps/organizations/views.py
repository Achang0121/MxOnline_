from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.operations.models import UserFavorite
from apps.organizations.models import CourseOrg, City, Teachers
from apps.organizations.forms import AddAskFrom


class OrgTeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teachers.objects.get(id=int(teacher_id))
        
        teacher_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                org_fav = True
        
        hot_teachers = Teachers.objects.order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'teacher_fav': teacher_fav,
            'org_fav': org_fav,
            'hot_teachers': hot_teachers,
        })


class OrgTeachersView(View):
    """讲师列表页"""
    
    def get(self, request, *args, **kwargs):
        all_teachers = Teachers.objects.all()
        teacher_nums = all_teachers.count()
        
        # 对讲师依照点击数进行排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
        
        hot_teachers = Teachers.objects.order_by('-click_nums')[:3]
        
        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        search_type = "teacher"
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords))

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=5, request=request)
        teachers = p.page(page)
        
        return render(request, 'teachers-list.html', {
            'teachers': teachers,
            'hot_teachers': hot_teachers,
            'teacher_nums': teacher_nums,
            'sort': sort,
            'keywords': keywords,
            'search_type': search_type,
        })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        
        is_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_fav = True
        
        return render(request, 'org-detail-desc.html', {
            'current_page': current_page,
            'course_org': course_org,
            'is_fav': is_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=org_id)
        course_org.click_nums += 1
        course_org.save()
        
        is_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_fav = True
        
        all_courses = course_org.courses_set.all()
        
        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        
        p = Paginator(all_courses, per_page=1, request=request)
        courses = p.page(page)
        
        return render(request, 'org-detail-course.html',
                      {
                          'all_courses': courses,
                          'current_page': current_page,
                          'course_org': course_org,
                          'is_fav': is_fav,
                      })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        
        is_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_fav = True
        
        all_teachers = course_org.teachers_set.all()
        
        return render(request, 'org-detail-teachers.html',
                      {
                          'all_teachers': all_teachers,
                          'course_org': course_org,
                          'current_page': current_page,
                          'is_fav': is_fav,
                      })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        
        is_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_fav = True
        
        all_courses = course_org.courses_set.all()[:3]
        all_teachers = course_org.teachers_set.all()[:1]
        return render(request, 'org-detail-homepage.html',
                      {
                          'all_courses': all_courses,
                          'all_teachers': all_teachers,
                          'course_org': course_org,
                          'current_page': current_page,
                          'is_fav': is_fav,
                      })


class AddAskView(View):
    """处理用户咨询"""
    
    def post(self, request, *args, **kwargs):
        user_ask_form = AddAskFrom(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return JsonResponse({
                "status": "success",
            })
        
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "提交出错~",
            })


class OrgView(View):
    def get(self, request, *args, **kwargs):
        # 从数据库里获取数据
        all_orgs = CourseOrg.objects.all()
        all_cities = City.objects.all()
        
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        
        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        search_type = "org"
        if keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords))
        
        # 通过机构类别对课程机构筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        
        # 通过机构所在城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))
        
        # 对机构排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            # 学习人数排序
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')
        
        org_nums = all_orgs.count()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)
        
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'hot_orgs': hot_orgs,
            'org_nums': org_nums,
            'all_cities': all_cities,
            'category': category,
            'city_id': city_id,
            'sort': sort,
            'keywords': keywords,
            'search_type': search_type,
        })
