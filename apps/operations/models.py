from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Courses
from apps.users.models import BaseModel

UserProfile = get_user_model()
FAV_TYPE = (
    (1, "课程"),
    (2, "机构"),
    (3, "讲师"),
)


class Banner(BaseModel):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m", max_length=200, verbose_name="轮播图")
    url = models.URLField(max_length=200, verbose_name="轮播图跳转URL")
    index = models.IntegerField(default=0, verbose_name="顺序")
    
    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.title


class UserAsk(BaseModel):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    
    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.name} {self.course_name} {self.mobile}"


class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="课程")
    comments = models.CharField(max_length=200, verbose_name="课程评论")
    
    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.comments


class UserFavorite(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(verbose_name="数据id")
    fav_type = models.IntegerField(choices=FAV_TYPE, default=1, verbose_name="收藏类型")
    
    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.user.username}_{self.fav_id}"


class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    message = models.CharField(max_length=200, verbose_name="消息内容")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    
    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.message


class UserCourses(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="课程")
    
    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.course.name
