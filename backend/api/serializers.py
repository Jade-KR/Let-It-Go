from rest_framework import serializers
from .models import Theme
from rest_auth.registration.serializers import RegisterSerializer

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = [
            'id',
            'parent_id',
            'name',
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