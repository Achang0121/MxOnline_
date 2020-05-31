from django.db import models
from django.utils.safestring import mark_safe

from DjangoUeditor.models import UEditorField
from apps.users.models import BaseModel
from apps.organizations.models import Teachers, CourseOrg

# Create your models here.

DEGREE_CHOICES = (
    ("primary", "初级"),
    ("middle", "中级"),
    ("senior", "高级"),
)


class Courses(BaseModel):
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, verbose_name="课程讲师")
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="课程机构")
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=10, verbose_name="难度")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default="后端开发", max_length=20, verbose_name="课程类别")
    tags = models.CharField(default="", max_length=10, verbose_name="课程标签")
    notice = models.CharField(default="", max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师有话说")
    
    detail = UEditorField(width=600,
                          height=300,
                          imagePath='courses/ueditor/image',
                          filePath='courses/ueidtor/files/',
                          default='',
                          verbose_name="课程详情",
                          )
    image = models.ImageField(upload_to="courses/%Y/%m", max_length=100, verbose_name="封面图")
    is_classics = models.BooleanField(default=False, verbose_name="是否是经典课程")
    is_banner = models.BooleanField(default=False, verbose_name="是否为广告位课程")
    
    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name
    
    def lesson_nums(self):
        return self.lessons_set.all().count()
    
    def show_image(self):
        # 在后台课程信息表中追加一段html来显示图片, 为防止图片大小不一样，统一设置了宽高，避免页面显示异常
        return mark_safe(f"<img src='{self.image.url}' width='240' height='135'>")
    
    def go_to(self):
        return mark_safe(f"<a href='/course/{self.id}'>传送门</a>")
    
    show_image.short_description = "图片"
    go_to.short_description = "传送门"


class BannerCourses(Courses):
    class Meta:
        verbose_name = "轮播课程信息"
        verbose_name_plural = verbose_name
        proxy = True


class CourseTag(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="课程")
    tag = models.CharField(max_length=100, verbose_name="课程标签")
    
    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.tag


class Lessons(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="外键->课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    
    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, verbose_name="外键->章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    url = models.CharField(max_length=1000, verbose_name="访问地址")
    
    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="外键->课程")
    name = models.CharField(max_length=100, verbose_name="资源名称")
    file = models.FileField(upload_to="courses/resource/%Y/%m", max_length=200, verbose_name="下载地址")
    
    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name
