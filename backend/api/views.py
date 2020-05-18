from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, Theme, LegoSet, OfficialMapping, Category, Review, LegoPart, Color, UserPart, SetPart
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
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    pagination_class = SmallPagination

class LegoSetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LegoSet.objects.all()
    serializer_class = serializers.LegoSetSerializer
    pagination_class = SmallPagination

class LegoPartViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LegoPart.objects.all()
    serializer_class = serializers.LegoPartSerializer
    pagination_class = SmallPagination

class UserInventoryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = UserPart.objects.all()

@api_view(['POST'])
def UpdateUserInventory(self):
    # user = self.user
    user = CustomUser.objects.get(id=1)
    if user.is_authenticated:
        # 요청 들어온 데이터 정리하기
        update_dict = dict()
        for update_part in self.data.get("LegoList"):
            if update_dict.get(update_part["part_id"]):
                if update_dict[update_part["part_id"]].get(update_part["color_id"]):
                    update_dict[update_part["part_id"]][update_part["color_id"]] += update_part["qte"]
                else:
                    update_dict[update_part["part_id"]][update_part["color_id"]] = update_part["qte"]
            else:
                update_dict[update_part["part_id"]] = {update_part["color_id"]: update_part["qte"]}
        
        # 유저 보유 데이터 정리하기
        inventory_dict = dict()
        for userpart in UserPart.objects.filter(user=user):
            inventory_dict[userpart.part_id] = {userpart.color_id: userpart.quantity}
        print(update_dict)
        print(inventory_dict)
        # # 정리된 데이터를 바탕으로 업데이트하기
        # for userpart in UserPart.objects.filter(user=user):
        #     tmp.add(userpart.part_id)
        # # 재고 있는 리스트 or 재고 없는데 양수
        # a = []
        # for userpart in data:
        #     if userpart["id"] in tmp or not userpart["qte"] < 0:
        #         a.append(userpart)
        #     else:
        #         b.append(userpart)


        # print(a)
        # print(b)
        # print(serializers.UserPartSerializer(UserPart.objects.filter(user=user), many=True).data)
        # UserPart.objects.create(user=user, part_id=data[0]["id"], color_id=data[0]["color"], quantity=data[0]["qte"])
    return Response("")
