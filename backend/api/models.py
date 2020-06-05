from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50)
    image = models.TextField(null=True)
    comment = models.CharField(max_length=300, null=True)
    age = models.IntegerField(default=30)
    gender = models.IntegerField(default=0)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
    review_count = models.IntegerField(default=0)
    categories = models.TextField(null=True)
    
    @property
    def category_list(self):
        return self.categories.split("|") if self.categories else ""

class Theme(models.Model):
    id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    root_id = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class LegoSet(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    num_parts = models.IntegerField(null=True)
    images = models.TextField(null=True)
    description = models.CharField(max_length=500, null=True)
    tags = models.CharField(max_length=200, null=True)
    references = models.CharField(max_length=500, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_sets", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    @property
    def tag_list(self):
        return self.tags.split("|") if self.tags else []
    @property
    def reference_list(self):
        return self.references.split("|") if self.references else []
    @property
    def image_list(self):
        return self.images.split("|") if self.images else []
    @property
    def image(self):
        return self.images.split("|")[0] if self.images else ""


    def __str__(self):
        return self.name

class OfficialMapping(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    lego_set = models.ForeignKey(LegoSet, on_delete=models.SET_NULL, null=True)

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    part_count = models.IntegerField()

    def __str__(self):
        return self.name

class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    lego_set = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class LegoPart(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True)
    image = models.TextField(null=True)
    bricklink_ids = models.TextField(null=True)
    official_ids = models.TextField(null=True)

    @property
    def bricklink_id_list(self):
        return self.bricklink_ids.split("|") if self.bricklink_ids else []

    @property
    def official_id_list(self):
        return self.official_ids.split("|") if self.official_ids else []

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
    def bricklink_id_list(self):
        return self.bricklink_ids.split("|") if self.bricklink_ids else []
    @property
    def bricklink_descrs_list(self):
        return self.bricklink_descrs.split("|") if self.bricklink_descrs else []
    @property
    def official_id_list(self):
        return self.official_ids.split("|") if self.official_ids else []
    @property
    def official_descrs_list(self):
        return self.official_descrs.split("|") if self.official_descrs else []

    def __str__(self):
        return self.name

class UserPart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    part = models.ForeignKey(LegoPart, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.part_id

class UserPart2(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    part = models.ForeignKey(LegoPart, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.part_id

class SetPart(models.Model):
    lego_set = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
    part = models.ForeignKey(LegoPart, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

class UserLikeLegoSet(models.Model):
    id = models.IntegerField(primary_key=True)
    customuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    legoset = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = 'api_legoset_like_users'

class UserSet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    legoset = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
    quantity = models.IntegerField()