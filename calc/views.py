# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# request.GET.get('key','没有时的默认值') 如果在字典类型中找不到key会报错
def sum(request):
    print('request get',request.GET)
    a = request.GET.get('a','')
    b = request.GET.get('b','')
    if not a or not b:
        return HttpResponse('请输入内容')
    c = int(a) + int(b)
    return HttpResponse(c)
