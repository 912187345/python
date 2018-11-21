# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import uuid
import os
import time
import Image

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST 
from django.core import serializers
from django import forms
from django.db import transaction

from django.forms.models import model_to_dict

from .models import Blog
from .models import User

from .common import serverReturn,commonConfig,sqlHandle,writeFile,deleteFile,Util,ImgChange

# Create your views here.
@require_POST
def login(request):
    param = request.jsonBody
    user = {
        'username':param['user'],
        'password':param['pwd']
    }
    query = User.objects.filter(username=user['username']).values().first()
    if query == None:
        pass
        return serverReturn.fail(errMsg="找不到用户名")
    else:
        pass
        if user['password'] == query['password']:
            del query['password']
            del query['userid']
            return serverReturn.success(data=query)
        else:
            return serverReturn.fail(errMsg="密码错误")

@require_POST
def register(request):
    param = request.jsonBody
    print('param',param)
    token = str(uuid.uuid4()).replace('-','')
    user = {
        'username':param['userName'],
        'password':param['pwd'],
        'sex':param['sex'],
        'email':param['email'],
        'token':token,
        'background':commonConfig['DEFAULT_USER_BACKGROUND']
    }
    if user['sex'] == 'boy':
        user['headImg'] = commonConfig['DEFAULT_BOY_ICON']
    else:
        user['headImg'] = commonConfig['DEFAULT_GIRL_ICON']

    #返回元祖类型
    reg = User.objects.get_or_create(username=user['username'],defaults=user)

    if reg[1] == True:
        # user['headImg'] = user['headimg']
        return serverReturn.success(data=user)
    else:
        return serverReturn.fail(errMsg='用户名已存在，请使用其他用户名')

@require_POST
def getBlogList(request):
    body = request.jsonBody
    if 'limit' in body:
        limit = body['limit'] or '10'
    if 'offset' in body:
        offset = body['offset'] or '0'
    try:
        pass
        data = sqlHandle('select * from get_list LIMIT ' + str(offset) + ',' + str(limit))
    except:
        pass
        return serverReturn.fail(errMsg='获取列表失败，请稍后重试')
    else:
        pass
        return serverReturn.success(data=data)

@require_POST
def editUserHead(request):
    #file_obj.multiple_chunks() = true时表示文件过大(默认 >2.5M，可配置)，需要分块进行处理

    token = request.POST.get('token')
    file_obj = request.FILES.get('file')
    baseDir = os.path.dirname(__file__)
    
    fileName = request.POST.get('token') + str(int(time.time())) + '.jpg'
    imgPath = os.path.join(baseDir,'static/userHeaderIcon',fileName)
    print('user header path',imgPath)
    user = User.objects.filter(token=token).values().first()
    
    if user['headImg'] != commonConfig['DEFAULT_BOY_ICON'] or user['headImg'] != commonConfig['DEFAULT_GIRL_ICON']:
        userHeadImgPath = os.getcwd()+ '/blog/static' + user['headImg']
        deleteFile(userHeadImgPath)

    try:
        writeFile(imgPath,file_obj)
    except:
        return serverReturn.fail(errMsg="更新头像失败，请重试")
    else:
        User.objects.filter(token=token).update(headImg='/userHeaderIcon/'+fileName)
        try:
            img = Image.open(imgPath)
            w,h =  img.size #返回的是元祖类型，可以按顺序赋值给变量
            dImg = img.resize((w/2,h/2))
            dImg.save(imgPath)
        except:
            print('压缩图片失败')
        return serverReturn.success(data={"headImg":'static/userHeaderIcon/'+fileName})

@require_POST
def editUserBG(request):

    token = request.POST.get('token')
    file_obj = request.FILES.get('file')
    baseDir = os.path.dirname(__file__)

    fileName = token + str(int(time.time())) + '.jpg'
    imgPath = os.path.join(baseDir,'static/bg',fileName)
    user = User.objects.filter(token=token).values().first()
    print('user image path',imgPath)
    if user['background'] != commonConfig['DEFAULT_USER_BACKGROUND']:
        userBackGroundPath = os.getcwd()+'/blog/static' + user['background']
        deleteFile(userBackGroundPath)

    try:
        writeFile(imgPath, file_obj)
    except:
        return serverReturn.fail(errMsg="更新背景失败，请重试")
    else:
        User.objects.filter(token=token).update(background="/bg/"+fileName)
        try:
            img = Image.open(imgPath)
            w,h = img.size
            dImg = img.resize((w/2,h/2))
            dImg.save(imgPath)
        except:
            print('压缩图片失败')
        return serverReturn.success(data={"background":"static/bg/"+fileName})

@require_POST
def getBlogById(request):
    pass
    param = request.jsonBody
    blogId = param['id']
    token = param['token']
    try:
        pass
        blog = Blog.objects.filter(blogid=blogId).first()
    except:
        return serverReturn.fail(errMsg="获取失败，请稍后重试") 
    
    blogDict = model_to_dict(blog)
    userDict = model_to_dict(blog.usertoken,exclude=['userid','password'])
    commentsList = serializers.serialize('json',blog.comments.all())
    
    data = {
        'blog':{
            'user':{},
            'comments':[]
        }
    }
    data = blogDict
    data['collection'] = {}
    data['user'] = userDict
    data['comments'] = []

    data['collection'] = {
        'collectionNum':len(blog.collection.all()),
        'collectionBol':True if len(blog.collection.filter(token=token)) > 0 else False
    }

    for comment in blog.comments.all():

        commentDict = model_to_dict(comment,exclude=['id'])
        commentDict['commentsUser'] = model_to_dict(
            comment.commentstoken,
            fields=['headImg','username'])

        commentDict['replycomments'] = []
        for reply in comment.replyComments.all():
            replyItem = model_to_dict(reply)
            replyItem['fromUser'] = model_to_dict(reply.fromtoken)
            replyItem['toUser'] = model_to_dict(reply.totoken)
            commentDict['replycomments'].append(replyItem)

        data['comments'].append(commentDict)

    return serverReturn.success(data=data)

@require_POST
def addBlog(reuqest):
    param = reuqest.jsonBody
    content = param['text']
    token = param['token']
    title = param['title']
    date = str(int(time.time()))
    newBlogId = date+str(token)

    htmlStr = ImgChange({'htmlStr':content,'fileName':newBlogId}).getHtmlStr()
    print('addBlog',htmlStr)
    return serverReturn.fail(errMsg="稍后重试")
    

@require_POST
def editBlog(request):
    print('editeBlog')

@require_POST
def collection(request):
    print('collec')

@require_POST
def getCollection(request):
    print('getCollection')

@require_POST
def blogComments(request):
    print('blogComments')

@require_POST
def deleteComments(request):
    print('deleteComments')

@require_POST
def replyComments(request):
    print('replyComments')