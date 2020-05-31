from django.db import models

from DjangoUeditor.models import UEditorField
from apps.users.models import BaseModel, UserProfile

# Create your models here.
COURSE_ORG_CHOICES = (
    ("pxjg", "培训机构"),
    ("gx", "高校"),
    ("gr", "个人"),
)


class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name="城市名")
    desc = models.CharField(max_length=200, verbose_name="描述")
    
    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name="课程机构")
    desc = UEditorField(width=600,
                        height=300,
                        default='',
                        imagePath='org/ueditor/images/',
                        filePath='org/ueditor/files/',
                        verbose_name="机构描述"
                        )
    tags = models.CharField(default="全国知名", max_length=10, verbose_name="机构标签")
    category = models.CharField(choices=COURSE_ORG_CHOICES, max_length=20, default="pxjg", verbose_name="机构类别")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", max_length=100, verbose_name="logo", null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    
    is_auth = models.BooleanField(default=False, verbose_name="是否认证")
    is_gold = models.BooleanField(default=False, verbose_name="是否金牌")
    
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")
    
    def courses(self):
        courses = self.courses_set.filter(is_classics=True)[:3]
        return courses
    
    class Meta:
        verbose_name = "授课机构"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class Teachers(BaseModel):
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, related_name='teacher', null=True, blank=True,
                                verbose_name="用户")
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="讲师姓名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", max_length=100, verbose_name="头像", null=True, blank=True)
    
    class Meta:
        verbose_name = "讲师"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name
    
    def course_nums(self):
        return self.courses_set.all().count()
