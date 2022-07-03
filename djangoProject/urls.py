"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

import account.views
import account.login
import account.searchAndBorrow
import account.user
urlpatterns = [
    path('login/',account.login.login),
path('image/code/',account.login.image_code),
    path('index/',account.views.index),
path('searchBook/',account.searchAndBorrow.searchBook),
path('borrowedBook/',account.searchAndBorrow.borrowedBook),
path('borrowedRecord/',account.searchAndBorrow.borrowedRecord),
re_path('adminBook/',account.views.adminBook,name="adminBook"),
path('adminUser/',account.views.adminUser),
path('adminRecord/',account.views.adminRecord),
path('adminAddBook/',account.views.adminAddBook.as_view()),
path('bookdetail/',account.searchAndBorrow.book_detail),
path('bookedit/',account.searchAndBorrow.book_edit),
path('deletebook/',account.searchAndBorrow.delete_book),
path('userdetail/',account.user.user_detail),
path('useredit/',account.user.user_edit),
path('deleteuser/',account.user.delete_user),
path('usernew/',account.user.user_new),
path('usereditpassword/',account.user.user_edit_password),
path('logout/',account.user.logout),
re_path(r'^$',account.searchAndBorrow.searchBook)
]
