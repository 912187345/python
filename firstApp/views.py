# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from blog.models import Blog
from django.db import connection

blogList = Blog.objects.values()
 
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    "print"
    print('desc',[col[0] for col in desc])
    return [
        dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
    ]

def sqlHandle(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    dic = dictfetchall(cursor)
    print('sql dic',dic)
    return dic

# Create your views here.
def index(request):
    print('first app index request',request)
    arr = ['jsonArr1','jsonArr2']
    obj = { 'title':'title', 'content':'content' }
    return render(request,'index.html',
        {
            'blogList':blogList,
            'arr':json.dumps(arr),
            'obj':json.dumps(obj),
            'list':blogList
        })

@require_POST
def getBlogList(request):
    body = json.loads(request.body)
    print('request.body',body['token'])
    data = {
        'data':sqlHandle('select * from get_list LIMIT 0,10'),
        'status':'success'
    }
    return HttpResponse(json.dumps(data))