from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LegoSet, LegoPart, Color, Review, CustomUser, Category, UserPart, SetPart, OfficialMapping, Theme

admin.site.register(LegoSet)
admin.site.register(LegoPart)
admin.site.register(Color)
admin.site.register(Review)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Category)
admin.site.register(UserPart)
admin.site.register(SetPart)
admin.site.register(OfficialMapping)
admin.site.register(Theme)
