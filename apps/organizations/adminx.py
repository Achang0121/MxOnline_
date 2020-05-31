import xadmin

from apps.organizations.models import Teachers, CourseOrg, City
from xadmin.layout import Main, Side, Fieldset, Row


class CourseOrgAdmin:
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']
    model_icon = 'fa fa-university'
    style_fields = {
        'desc': 'ueditor',
    }
    
    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset('机构信息',
                         'name', 'city',
                         Row('category', 'tags', 'course_nums'),
                         'image', 'address', 'desc',
                         ),
            ),
            Side(
                Fieldset('访问信息',
                         'fav_nums', 'click_nums', 'students', 'add_time',
                         ),
            ),
            Side(
                Fieldset('选择信息',
                         'is_gold', 'is_auth',
                         ),
            ),
        )
        return super(CourseOrgAdmin, self).get_form_layout()


class TeachersAdmin:
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']
    list_editable = ["name", ]
    
    model_icon = 'fa fa-mortar-board'
    
    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset('基本信息',
                         'image',
                         Row('name', 'age'),
                         'user',
                         'points',
                         ),
                Fieldset('工作信息',
                         Row('work_company', 'work_position'),
                         Row('work_years', 'org'),
                         ),
            ),
            Side(
                Fieldset('访问信息',
                         'fav_nums', 'click_nums', 'add_time',
                         ),
            ),
        )
        return super(TeachersAdmin, self).get_form_layout()


class CityAdmin:
    list_display = ['id', 'name', 'desc']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    list_editable = ['name', 'desc']
    model_icon = 'fa fa-paper-plane'


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teachers, TeachersAdmin)
xadmin.site.register(City, CityAdmin)
