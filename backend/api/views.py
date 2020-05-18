from django.shortcuts import render, get_object_or_404, redirect
from api import models, serializers
from rest_framework import viewsets, mixins
from rest_framework.schemas import AutoSchema
from rest_framework.decorators import api_view, action, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class ThemeViewSet(viewsets.ModelViewSet): 
    queryset = models.Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    pagination_class = SmallPagination

class LegoSetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.LegoSet.objects.all()
    serializer_class = serializers.LegoSetSerializer
    pagination_class = SmallPagination
