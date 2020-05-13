from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    nickName = models.CharField(max_length=50)
    image = models.TextField(null=True)
    comment = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    gender = models.IntegerField(null=True)
    parts = models.TextField(null=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')

class LegoSet(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    parts = models.TextField(null=True)
    images = models.TextField(null=True)
    description = models.CharField(max_length=500, null=True)
    tags = models.CharField(max_length=200, null=True)
    references = models.CharField(max_length=500, null=True)
    likeUsers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likeSets", blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    @property
    def tagList(self):
        return self.tags.split("|") if self.tags else []
    @property
    def referenceList(self):
        return self.references.split("|") if self.references else []
    @property
    def imageList(self):
        return self.images.split("|") if self.images else []

    def __str__(self):
        return self.name

class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    setId = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class LegoPart(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    image = models.TextField(null=True)
    bricklinkIds = models.TextField(null=True)

    @property
    def bricklinkIdList(self):
        return self.bricklinkIds.split("|") if self.bricklinkIds else []

    def __str__(self):
        return self.name

class Color(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    rgb = models.TextField(null=True)
    bricklinkIds = models.TextField(null=True)
    bricklinkDescrs = models.TextField(null=True)
    officialIds = models.TextField(null=True)
    officialDescrs = models.TextField(null=True)

    @property
    def bricklinkIdList(self):
        return self.bricklinkIds.split("|") if self.bricklinkIds else []
    @property
    def bricklinkDescrsList(self):
        return self.bricklinkDescrs.split("|") if self.bricklinkDescrs else []
    @property
    def officialIdList(self):
        return self.officialIds.split("|") if self.officialIds else []
    @property
    def officialDescrsList(self):
        return self.officialDescrs.split("|") if self.officialDescrs else []

    def __str__(self):
        return self.name