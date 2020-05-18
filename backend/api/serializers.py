from .models import CustomUser, Theme, LegoSet, OfficialMapping, Category, Review, LegoPart, Color, UserPart, SetPart
from rest_framework import serializers

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = [
            "id",
            "parent_id",
            "name",
        ]

class LegoSetSerializer(serializers.ModelSerializer):
    # theme_detail = ThemeSerializer(source="theme")
    # set_pk, set_name, image,user_name, user_like
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = LegoSet
        fields = [
            "id",
            "name",
            "nickname",
            "image",
            #좋아요여부
        ]
    def get_nickname(self, obj):
        return obj.user.nickname if obj.user else "Official Set"

class LegoPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegoPart
        fields = [
            "id",
            "category",
            "name",
            "image",
        ]

class UserPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPart
        fields = [
            "user_id",
            "part_id",
            "color_id",
            "quantity"
        ]