# Generated by Django 4.0.5 on 2022-06-18 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_book_imgdir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='chinaclass',
            field=models.CharField(max_length=30, verbose_name='中图分类号'),
        ),
    ]
