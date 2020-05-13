from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50)
    user_image = models.TextField(null=True)
    comment = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    gender = models.IntegerField(null=True)
    user_parts = models.TextField(null=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')

class Lego_set(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    set_name = models.CharField(max_length=100, null=True)
    set_parts = models.TextField(null=True)
    set_image = models.TextField(null=True)
    description = models.CharField(max_length=500, null=True)
    tags = models.CharField(max_length=200, null=True)
    references = models.CharField(max_length=500, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_sets", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def tag_list(self):
        return self.tags.split("|") if self.tags else []
    @property
    def reference_list(self):
        return self.references.split("|") if self.references else []

    def __str__(self):
        return self.set_name

class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    set_id = models.ForeignKey(Lego_set, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Lego_part(models.Model):
    id = models.IntegerField(primary_key=True)
    part_name = models.CharField(max_length=100, null=True)
    part_image = models.TextField(null=True)
    bricklink_ids = models.TextField(null=True)

    @property
    def bricklink_ids_list(self):
        return self.bricklink_ids.split("|") if self.bricklink_ids else []

    def __str__(self):
        return self.part_name

class Color(models.Model):
    id = models.IntegerField(primary_key=True)
    color_name = models.CharField(max_length=100, null=True)
    color_rgb = models.TextField(null=True)
    bricklink_ids = models.TextField(null=True)
    bricklink_descrs = models.TextField(null=True)
    official_ids = models.TextField(null=True)
    official_descrs = models.TextField(null=True)

    @property
    def bricklink_ids_list(self):
        return self.bricklink_ids.split("|") if self.bricklink_ids else []
    @property
    def bricklink_descrs_list(self):
        return self.bricklink_descrs.split("|") if self.bricklink_descrs else []
    @property
    def official_ids_list(self):
        return self.official_ids.split("|") if self.official_ids else []
    @property
    def official_descrs_list(self):
        return self.official_descrs.split("|") if self.official_descrs else []

    def __str__(self):
        return self.color_name