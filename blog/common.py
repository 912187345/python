# -*- coding: utf-8 -*-
import json
import os
from HTMLParser import HTMLParser

from django.http import HttpResponse
from django.db import connection

commonConfig = {
        'blogImgPath':'./static/blogImage/',
        'FAIL':'fail',
        'SUCCESS':'success',
        'DEFAULT_BOY_ICON':'static/userHeaderIcon/head_boy.png',
        'DEFAULT_GIRL_ICON':'static/userHeaderIcon/head_girl.png',
        'DEFAULT_USER_BACKGROUND':'static/bg/DEFAULT_BG.jpg',
        'URL':'http://192.168.1.201:8086',
        'userHeaderPath':'/static/userHeaderIcon/',
        'userBGPath':'/static/userHeaderIcon'
    }

class serverReturn(object):
    
    @staticmethod
    def success(**kw):
        data = {
            'status':'success'
        }
        if 'data' in kw:
            data['data'] = kw['data']
        return HttpResponse(json.dumps(data)) 

    @staticmethod
    def fail(**kw):
        data = {
            'status':'fail'
        }
        if 'data' in kw:
            data['data'] = kw['data']
        if 'errMsg' in kw:
            data['errMsg'] = kw['errMsg']
        return HttpResponse(json.dumps(data))
    
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

def deleteFile(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        return "file not exists"

def writeFile(path,fileObj):
    f = open(path,'wb')
    if fileObj.multiple_chunks() == True:
        for chunk in fileObj.multiple_chunks():
            f.write(chunk)
        f.close()
    else:
        f.write(fileObj.read())
        f.close()

class Util(object):
    import os
    from django.db import connection
    
    def dictfetchall(self,cursor):
        return dictfetchall(cursor)

    def sqlHandle(self,sql):
        return sqlHandle(sql)

    def writeFile(self,path,fileObj):
        return writeFile(path,fileObj)

    def deleteFile(self,path):
        return deleteFile(path)

class htmlHandle(HTMLParser):
    def __init__(self):
        print('aa')

class ImgChange(Util):
        
    htmlStr = ''
    fileName = ''
    img = []
    def __init__(self,obj):
        print('ImgChange init')
        self.htmlStr = obj['htmlStr']
        self.fileName = obj['fileName']
    def changeImg(self):
        return ''
    def loadImg(self,img):
        return '' 