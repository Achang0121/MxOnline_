# Generated by Django 2.2 on 2020-05-30 06:43

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_bannercourses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='课程详情'),
        ),
    ]
