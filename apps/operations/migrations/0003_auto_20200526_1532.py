# Generated by Django 2.2 on 2020-05-26 15:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0002_auto_20200518_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('image', models.ImageField(max_length=200, upload_to='banner/%Y/%m', verbose_name='轮播图')),
                ('url', models.URLField(verbose_name='轮播图跳转URL')),
                ('index', models.IntegerField(default=0, verbose_name='顺序')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_type',
            field=models.IntegerField(choices=[(1, '课程'), (2, '机构'), (3, '讲师')], default=1, verbose_name='收藏类型'),
        ),
    ]