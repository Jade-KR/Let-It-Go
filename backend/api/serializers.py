from .models import CustomUser, Theme, LegoSet, OfficialMapping, Category, Review, LegoPart, Color, UserPart, SetPart
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from api import views

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = [
            "id",
            "parent_id",
            "name",
        ]

class ReviewSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = [
            "user_id",
            "nickname",
            "content",
            "score",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname

class SetPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetPart
        fields = [
            "lego_set_id",
            "part_id",
            "color_id",
            "quantity"
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
            "images",
            "review_count",
            "like_count",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname if obj.user else "Official Set"
    # def get_image(self, obj):
    #     return obj.images[0] if obj.images else ""

class LegoSetSerializer2(serializers.ModelSerializer):
    reviews = ReviewSerializer(source="review_set", many=True)
    nickname = serializers.SerializerMethodField()
    parts = serializers.SerializerMethodField()
    class Meta:
        model = LegoSet
        fields = [
            "id",
            "name",
            "nickname",
            "user_id",
            "images",
            "parts",
            "reviews",
            "description",
            "tags",
            "theme",
            "review_count",
            "like_count",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname if obj.user else "Official Set"
    def get_image(self, obj):
        return obj.images[0] if obj.images else ""
    def get_parts(self, obj):
        views.crawling_part_data(obj.id)
        return SetPartSerializer(LegoSet.objects.get(id=obj.id).setpart_set.all(), many=True).data

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
    image = serializers.SerializerMethodField()
    rgb = serializers.SerializerMethodField()
    class Meta:
        model = UserPart
        fields = [
            "user_id",
            "part_id",
            "color_id",
            "quantity",
            "image",
            "rgb",
        ]
    def get_image(self, obj):
        return LegoPart.objects.filter(id=obj.part_id)[0].image if LegoPart.objects.filter(id=obj.part_id) else ""
    def get_rgb(self, obj):
        return Color.objects.get(id=obj.color_id).rgb

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=50)
    image = serializers.CharField(required=False)
    comment = serializers.CharField(max_length=300, required=False)
    age = serializers.IntegerField(required=False)
    gender = serializers.IntegerField(required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        data_dict['image'] = self.validated_data.get('image', '')
        data_dict['comment'] = self.validated_data.get('comment', '')
        data_dict['age'] = self.validated_data.get('age', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        return data_dict


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "nickname",
            "image"
        ]

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "nickname",
            "image",
            "comment",
        ]