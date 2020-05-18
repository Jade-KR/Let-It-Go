from django.shortcuts import render, get_object_or_404, redirect
from api import models, serializers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class ThemeViewSet(viewsets.ModelViewSet): 
    queryset = models.Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    pagination_class = SmallPagination
