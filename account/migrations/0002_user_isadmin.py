# Generated by Django 4.0.5 on 2022-06-18 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isadmin',
            field=models.BooleanField(default=False, verbose_name='管理员账户'),
        ),
    ]