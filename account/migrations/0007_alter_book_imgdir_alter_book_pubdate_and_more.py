# Generated by Django 4.0.5 on 2022-06-20 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_book_onboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='imgdir',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='图片路径'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pubdate',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='出版日期'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=30, unique=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, unique=True, verbose_name='用户名'),
        ),
    ]