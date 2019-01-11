# -*- coding: utf-8 -*-
import os,json,base64,re
from HTMLParser import HTMLParser

from django.http import HttpResponse
from django.db import connection

commonConfig = {
        'blogImgPath':'static/blogImage/',
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

def deleteOldImg(oldText,newText):
    print('deleteOldImg')
    parseImg = HtmlHandle()

    parseImg.feed(oldText or '<div></div>')
    oldImgSrcArray = parseImg.getImg()
    
    parseImg.feed(newText or '<div></div>')
    newImgSrcArray = parseImg.getImg()

    if len(oldImgSrcArray) == 0:
        return "didn't delete"

    for imgSrc in oldImgSrcArray:
        try:
            newImgSrcArray.index(imgSrc)
        except:
            pass
        else:
            deleteFile(imgSrc)
        

class HtmlHandle(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.imgArr = []
    def handle_starttag(self,tag,attrs):
        if tag == 'img' and attrs[0][0] == 'src':
            print(attrs[0][1])
            self.imgArr.append(attrs[0][1])
    def getImg(self):
        return self.imgArr

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
    
    def htmlHandle(self):
        return HtmlHandle()

class ImgChange(Util):

    def __init__(self,obj):
        self.htmlStr = obj['htmlStr']
        self.fileName = obj['fileName']

    def getHtmlStr(self):
        imgArr = self.getImg(self.htmlStr)
        if len(imgArr) == 0:
            return self.htmlStr
        for i,imgSrc in enumerate(imgArr):
            if re.match(r'^data:image\/\w+;base64,',imgSrc) == None:
                continue
            base64 = re.sub(r'^data:image\/\w+;base64,','',imgSrc)
            imgPath = self.loadImg(base64,i)
            self.htmlStr = self.htmlStr.replace(imgSrc,imgPath)
        return self.htmlStr
    
    def loadImg(self,img,num):
        baseDir = os.path.dirname(__file__)
        path = os.path.join(baseDir,commonConfig['blogImgPath'], self.fileName) + str(num) + '.jpg'
        f = open(path,"wb")
        f.write(base64.b64decode(img))
        f.close()
        return path.replace(baseDir,'')
    
    def getImg(self,htmlStr):
        img = self.htmlHandle()
        img.feed(htmlStr)
        return img.getImg()
        
