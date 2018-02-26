# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from time import time
# Create your models here.

class UploadFile(models.Model):
    docfile = models.FileField(upload_to='upload/%Y/%m/%d')

class keyword(models.Model):
    id = models.BigAutoField(primary_key=True)
    keyword = models.CharField(max_length=200)
    click_number = models.BigIntegerField()
    updated_at = models.BigIntegerField()
    created_at = models.BigIntegerField()
    is_private = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.keyword

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = time()
        self.updated_at = time()

        if not self.is_private:
            self.is_private = 0

        super().save(*args,**kwargs)


class content(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    updated_at = models.BigIntegerField()
    created_at = models.BigIntegerField()

    def __str__(self):
        return self.content[0:200]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = time()
        self.updated_at = time()
        super().save(*args,**kwargs)


class keywordContent(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_keyword = models.BigIntegerField()
    id_content = models.BigIntegerField()
    updated_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['id_content']),
            models.Index(fields=['id_keyword']),
        ]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = time()
        self.updated_at = time()
        super().save(*args,**kwargs)


class keywordkeyword(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_keyword_parent = models.BigIntegerField()
    id_keyword = models.BigIntegerField()
    updated_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['id_keyword_parent']),
            models.Index(fields=['id_keyword']),
        ]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = time()
        self.updated_at = time()
        super().save(*args,**kwargs)


class keywordExtraLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_keyword_1 = models.BigIntegerField()
    id_keyword_2 = models.BigIntegerField()
    desc = models.CharField(max_length=200, default='normal')
    updated_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['id_keyword_1']),
            models.Index(fields=['id_keyword_2']),
        ]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = time()
        self.updated_at = time()
        super().save(*args,**kwargs)

