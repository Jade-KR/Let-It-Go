from django.shortcuts import render, get_object_or_404, redirect
from api import models, serializers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_auth.views import LoginView


class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class ThemeViewSet(viewsets.ModelViewSet):
    queryset = models.Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    pagination_class = SmallPagination

class CustomLoginView(LoginView):
    def get_response(self):
        user = get_object_or_404(models.CustomUser, username=self.user)
        orginal_response = super().get_response()
        mydata = {
            "nickname": user.nickname,
            "image": user.image,
            "comment": user.comment,
            "age": user.age,
            "gender": user.gender,
            "status": "success",
            }
        orginal_response.data["user"].update(mydata)
        return orginal_response