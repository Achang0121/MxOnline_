import xadmin

from apps.courses.models import Courses, Lessons, Video, CourseResource, CourseTag, BannerCourses
from import_export import resources
from xadmin.layout import Main, Fieldset, Row, Side


class LessonsInline:
    model = Lessons
    extra = 0
    # style = 'tab'


class VideoInline:
    model = Video
    extra = 0
    style = 'tab'


class CourseResourceInline:
    model = CourseResource
    extra = 1
    style = 'tab'


class CourseTagAdmin:
    list_display = ['course', 'tag', 'add_time']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_time']
    model_icon = 'fa fa-tags'


class GlobalSettings:
    site_title = "MxOnline后台管理系统"
    site_footer = "MxOnline"
    menu_style = "accordion"


class BaseSettings:
    # 主题修改
    enable_themes = True
    use_bootswatch = True


class CoursesResource(resources.ModelResource):
    class Meta:
        model = Courses


class CoursesAdmin:
    import_export_args = {
        'import_resource_class': CoursesResource,
        'export_resource_class': CoursesResource,
    }
    list_display = ['name', 'desc', 'show_image', 'go_to', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]
    readonly_fields = ['click_nums', 'fav_nums', 'students', 'add_time']  # 只读字段，即不可修改
    exclude = []  # 不显示的字段
    ordering = ['-click_nums']  # 按照某个字段排序后显示
    model_icon = 'fa fa-bookmark'
    
    inlines = [LessonsInline, CourseResourceInline]
    style_fields = {
        'detail': 'ueditor',
    }
    
    def queryset(self):
        qs = super(CoursesAdmin, self).queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs
    
    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset('讲师信息',
                         'teacher', 'course_org',
                         css_class='unsort no_title'
                         ),
                Fieldset('基本信息',
                         'name', 'desc',
                         Row('degree', 'learn_times'),
                         Row('category', 'tags'),
                         'notice', 'teacher_tell', 'detail',
                         ),
            ),
            Side(
                Fieldset('访问信息',
                         'fav_nums', 'click_nums', 'students', 'add_time',
                         ),
            ),
            Side(
                Fieldset('选择信息',
                         'is_banner', 'is_classics',
                         ),
            )
        )
        return super(CoursesAdmin, self).get_form_layout()


class BannerCoursesAdmin:
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]
    model_icon = 'fa fa-book'
    
    def queryset(self):
        qs = super(BannerCoursesAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs
    
    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset('讲师信息',
                         'teacher', 'course_org',
                         css_class='unsort no_title'
                         ),
                Fieldset('基本信息',
                         'name', 'desc',
                         Row('degree', 'learn_times'),
                         Row('category', 'tags'),
                         'notice', 'teacher_tell', 'detail',
                         ),
            ),
            Side(
                Fieldset('访问信息',
                         'fav_nums', 'click_nums', 'students', 'add_time',
                         ),
            ),
            Side(
                Fieldset('选择信息',
                         'is_banner', 'is_classics',
                         ),
            )
        )
        return super(BannerCoursesAdmin, self).get_form_layout()


class LessonsAdmin:
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fa fa-file'
    inlines = [VideoInline, ]


class VideoAdmin:
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']
    model_icon = 'fa fa-file-video-o'


class CourseResourceAdmin:
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']
    model_icon = 'fa fa-link'


xadmin.site.register(Courses, CoursesAdmin)
xadmin.site.register(BannerCourses, BannerCoursesAdmin)
xadmin.site.register(Lessons, LessonsAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
