from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50)
    image = models.TextField(null=True)
    comment = models.CharField(max_length=300, null=True)
    age = models.IntegerField(null=True)
    gender = models.IntegerField(null=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')

class LegoSet(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    images = models.TextField(null=True)
    description = models.CharField(max_length=500, null=True)
    tags = models.CharField(max_length=200, null=True)
    references = models.CharField(max_length=500, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_sets", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

class OfficialMapping(models.Model):
    set_id = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
    official_id = models.IntegerField()

    def __str__(self):
        return self.set_id

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    part_count = models.IntegerField()

    def __str__(self):
        return self.name

class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    set_id = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class LegoPart(models.Model):
    id = models.IntegerField(primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    image = models.TextField(null=True)
    bricklink_ids = models.TextField(null=True)

    @property
    def bricklinkIdList(self):
        return self.bricklink_ids.split("|") if self.bricklink_ids else []

    def __str__(self):
        return self.name

class Color(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    rgb = models.TextField(null=True)
    bricklink_ids = models.TextField(null=True)
    bricklink_descrs = models.TextField(null=True)
    official_ids = models.TextField(null=True)
    official_descrs = models.TextField(null=True)

    @property
    def bricklinkIdList(self):
        return self.bricklink_ids.split("|") if self.bricklink_ids else []
    @property
    def bricklinkDescrsList(self):
        return self.bricklink_descrs.split("|") if self.bricklink_descrs else []
    @property
    def officialIdList(self):
        return self.official_ids.split("|") if self.official_ids else []
    @property
    def officialDescrsList(self):
        return self.official_descrs.split("|") if self.official_descrs else []

    def __str__(self):
        return self.name

class UserPart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    part_id = models.ForeignKey(LegoPart, on_delete=models.CASCADE)
    color_id = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.part_id

class SetPart(models.Model):
    set_id = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
    part_id = models.ForeignKey(LegoPart, on_delete=models.CASCADE)
    color_id = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return self.set_id