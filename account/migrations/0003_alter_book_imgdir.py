# Generated by Django 4.0.5 on 2022-06-18 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_isadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='imgdir',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
