from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Lego_set, Lego_part, Color, Review, CustomUser

admin.site.register(Lego_set)
admin.site.register(Lego_part)
admin.site.register(Color)
admin.site.register(Review)
admin.site.register(CustomUser, UserAdmin)
