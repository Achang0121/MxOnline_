import xadmin

from apps.operations.models import CourseComments, UserAsk, UserCourses, UserFavorite, UserMessage, Banner


class BannerAdmin:
    list_display = ['title', 'image', 'url', 'index']
    search_fields = ['title', 'url', 'index']
    list_filter = ['title', 'index', 'add_time']
    model_icon = 'fa fa-spinner fa-spin'


class CourseCommentsAdmin:
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']
    model_icon = 'fa fa-comments'


class UserAskAdmin:
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    model_icon = 'fa fa-mortar-board'


class UserCoursesAdmin:
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']
    model_icon = 'fa fa-user-secret'
    
    def save_models(self):
        obj = self.new_obj
        if not obj.id:
            # 新增用户课程信息的拦截
            obj.save()
            course = obj.course
            course.students += 1
            course.save()


class UserFavoriteAdmin:
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fa fa-heart'


class UserMessageAdmin:
    list_display = ['user', 'message', 'is_read', 'add_time']
    search_fields = ['user', 'message', 'is_read']
    list_filter = ['user', 'message', 'is_read', 'add_time']
    model_icon = 'fa fa-comments-o'


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourses, UserCoursesAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
