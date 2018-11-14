# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext as _

class Blog(models.Model):
    text = models.TextField(_('博客'),max_length=255,blank=True)
    date = models.DateTimeField(blank=True, null=True)

    usertoken = models.ForeignKey(
        'User',
        db_column='userToken',
        to_field="token",
        related_name="user",
        max_length=255,
        blank=True,
        null=True,
        )  # Field name made lowercase.
    
    blogid = models.CharField(db_column='blogId', max_length=255, blank=True, null=True, unique=True)  # Field name made lowercase.
    title = models.CharField(max_length=255, blank=True, null=True)
    updatetime = models.DateTimeField(db_column='updateTime', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(max_length=255, blank=True,primary_key=True)
    # user = models.ForeignKey(
    #     'User',
    #     to_field="token",
    #     on_delete=models.CASCADE,
    #     related_name='user',
    #     blank=True,
    # )
    def __str__(self):
        return self.title
    class Meta:
        managed = False
        db_table = 'blog'


class Collection(models.Model):
    blogid = models.ForeignKey(
        'Blog',
        db_column='blogId',
        to_field='blogid',
        related_name='collection',
        max_length=255,
        blank=True, 
        null=True)  # Field name made lowercase.

    token = models.CharField(
        max_length=255,
        blank=True, 
        null=True)

    class Meta:
        managed = False
        db_table = 'collection'


class Comments(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    commentscontent = models.CharField(db_column='commentsContent', max_length=255, blank=True, null=True)  # Field name made lowercase.
    blogid = models.ForeignKey(
        'Blog',
        related_name="comments",
        to_field='blogid',
        db_column='blogId', 
        max_length=255, 
        blank=True, 
        null=True)  # Field name made lowercase.
    id = models.CharField(max_length=255, blank=True,primary_key=True)
    commentstoken = models.ForeignKey(
        'User',
        to_field='token',
        related_name='commentsUser',
        db_column='commentsToken', 
        max_length=255, 
        blank=True, 
        null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comments'


class Replycomments(models.Model):
    replytext = models.CharField(db_column='replyText', max_length=255, blank=True, null=True)  # Field name made lowercase.
    replydate = models.DateTimeField(db_column='replyDate', blank=True, null=True)  # Field name made lowercase.
    commentsid = models.ForeignKey(
        'Comments',
        to_field='id',
        db_column='commentsId', 
        related_name="replyComments",
        max_length=255, 
        blank=True,     
        null=True)  # Field name made lowercase.

    totoken = models.ForeignKey(
        'User',
        related_name='toUser',
        db_column='toToken',
        to_field='token',
        max_length=255, 
        blank=True, 
        null=True)  # Field name made lowercase.
    
    fromtoken = models.ForeignKey(
        'User',
        related_name='fromUser',
        to_field='token', 
        db_column='fromToken',
        max_length=255, 
        blank=True, 
        null=True)  # Field name made lowercase.
    blogid = models.CharField(db_column='blogId', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'replycomments'


class User(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    userid = models.AutoField(primary_key=True)
    sex = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True, unique=True)
    headImg = models.CharField(db_column='headImg', max_length=255, blank=True, null=True)  # Field name made lowercase.
    background = models.CharField(max_length=255, blank=True, null=True)
    registerdate = models.DateTimeField(db_column='registerDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    def __str__(self):
        return self.username
    class Meta:
        managed = False
        db_table = 'user'
