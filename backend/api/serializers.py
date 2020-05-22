from .models import CustomUser, Theme, LegoSet, OfficialMapping, Category, Review, LegoPart, Color, UserPart, SetPart
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

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

class SetPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetPart
        fields = [
            "lego_set_id",
            "part_id",
            "color_id",
            "quantity"
        ]

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
