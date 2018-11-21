# -*- coding: UTF-8 -*-
"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# 引入另一个应用的视图
from firstApp import views as firstApp_views
from calc import views as calc_views
from blog import views as blog_views


urlpatterns = [
    url('index', firstApp_views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^sum/$', calc_views.sum, name='sum'),
    url('register', blog_views.register, name='register'),
    url('logon',blog_views.login,name="login"),
    url('usersetting/upload-head-image',blog_views.editUserHead,name="uploadHeadImage"),
    url('usersetting/set-background',blog_views.editUserBG,name="uploadUserBackGround"),
    url(u'blog/get-blog-by-id',blog_views.getBlogById,name="getBlogById"),
    url(u'blog/get-blog', blog_views.getBlogList, name='getBlogList'),
    url(u'blog/add-blog', blog_views.addBlog, name='addBlog')
]