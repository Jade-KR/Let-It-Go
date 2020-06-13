from .models import CustomUser, Theme, LegoSet, OfficialMapping, Category, Review, LegoPart, Color, UserPart, SetPart, UserLikeLegoSet, UserSet
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
    user_image = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "user_id",
            "nickname",
            "content",
            "score",
            "user_image",
            "updated_at",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname
    def get_user_image(self, obj):
        return obj.user.image

class SetPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetPart
        fields = [
            "lego_set_id",
            "part_id",
            "color_id",
            "quantity"
        ]

class SetPartSerializer2(serializers.ModelSerializer):
    class Meta:
        model = SetPart
        fields = [
            "part_id",
            "color_id",
            "quantity"
        ]

class LegoSetSerializer(serializers.ModelSerializer):
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
    sub_sets = serializers.SerializerMethodField()
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
            "sub_sets",
        ]
    def get_sub_sets(self, obj):
        queryset = []
        for subset in obj.sub_set.all():
            queryset.append(subset.subset)
        return LegoSetSerializer(queryset, many=True).data
    def get_nickname(self, obj):
        return obj.user.nickname if obj.user else "Official Set"
    def get_image(self, obj):
        return obj.images[0] if obj.images else ""
    def get_parts(self, obj):
        # if not SetPart.objects.filter(lego_set=obj):
        #     views.crawling_part_data(obj.id)
        return SetPartSerializer2(obj.setpart_set.all(), many=True).data

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

class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "nickname",
            "age",
            "gender",
            "is_staff",
            "is_active",
            "last_login"
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

class UserSetSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    user_nickname = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    is_review = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    class Meta:
        model = UserSet
        fields = [
            "legoset_id",
            "quantity",
            "image",
            "name",
            "user_nickname",
            "is_like",
            "is_review",
            "like_count",
            "review_count",
        ]
    def get_image(self, obj):
        return obj.legoset.image
    def get_name(self, obj):
        return obj.legoset.name
    def get_user_nickname(self, obj):
        return obj.user.nickname
    def get_is_like(self, obj):
        return 1 if UserLikeLegoSet.objects.filter(customuser_id=obj.user_id, legoset_id=obj.legoset_id) else 0
    def get_is_review(self, obj):
        return 1 if Review.objects.filter(lego_set_id=obj.legoset_id, user_id=obj.user_id) else 0
    def get_like_count(self, obj):
        return obj.legoset.like_count
    def get_review_count(self, obj):
        return obj.legoset.review_count