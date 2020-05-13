from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LegoSet, LegoPart, Color, Review, CustomUser

admin.site.register(LegoSet)
admin.site.register(LegoPart)
admin.site.register(Color)
admin.site.register(Review)
admin.site.register(CustomUser, UserAdmin)
